"""Pygame renderer for Wave Function Collapse visualization."""

import pygame
from typing import Optional, Tuple, Dict
from .core import WaveFunctionCollapse, Cell
from .tiles import TileSet, TileType


class WFCRenderer:
    """Handles rendering WFC grids using Pygame."""
    
    def __init__(self, screen: pygame.Surface, tileset: TileSet, 
                 tile_size: int = 20, offset: Tuple[int, int] = (0, 0)):
        self.screen = screen
        self.tileset = tileset
        self.tile_size = tile_size
        self.offset_x, self.offset_y = offset
        
        # Colors for different states
        self.colors = {
            'unknown': (64, 64, 64),      # Dark gray for uncollapsed cells
            'border': (32, 32, 32),       # Border color
            'text': (255, 255, 255),      # White text
            'entropy_bg': (128, 0, 128),  # Purple background for entropy display
        }
        
        # Font for displaying entropy numbers
        pygame.font.init()
        self.font = pygame.font.Font(None, max(12, tile_size // 2))
    
    def render_grid(self, wfc: WaveFunctionCollapse, show_entropy: bool = False, 
                   show_borders: bool = True):
        """Render the entire WFC grid."""
        for y in range(wfc.height):
            for x in range(wfc.width):
                self.render_cell(wfc.grid[y][x], show_entropy, show_borders)
    
    def render_cell(self, cell: Cell, show_entropy: bool = False, 
                   show_border: bool = True):
        """Render a single cell."""
        # Calculate screen position
        screen_x = self.offset_x + cell.x * self.tile_size
        screen_y = self.offset_y + cell.y * self.tile_size
        
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        
        if cell.collapsed:
            # Render collapsed cell with tile color
            tile_type = next(iter(cell.possibilities))
            color = self.tileset.get_tile(tile_type).color
            pygame.draw.rect(self.screen, color, rect)
        else:
            # Render uncollapsed cell
            if show_entropy and cell.entropy > 0:
                # Color based on entropy (higher entropy = more red)
                max_entropy = len(self.tileset.get_all_types())
                entropy_ratio = cell.entropy / max_entropy
                red = int(255 * entropy_ratio)
                blue = int(255 * (1 - entropy_ratio))
                color = (red, 0, blue)
                pygame.draw.rect(self.screen, color, rect)
                
                # Draw entropy number
                self.render_entropy_text(cell, screen_x, screen_y)
            else:
                # Default unknown color
                pygame.draw.rect(self.screen, self.colors['unknown'], rect)
        
        # Draw border
        if show_border:
            pygame.draw.rect(self.screen, self.colors['border'], rect, 1)
    
    def render_entropy_text(self, cell: Cell, screen_x: int, screen_y: int):
        """Render entropy number on a cell."""
        if cell.entropy == 0:
            return
        
        text = str(cell.entropy)
        text_surface = self.font.render(text, True, self.colors['text'])
        text_rect = text_surface.get_rect()
        
        # Center the text in the cell
        text_x = screen_x + (self.tile_size - text_rect.width) // 2
        text_y = screen_y + (self.tile_size - text_rect.height) // 2
        
        self.screen.blit(text_surface, (text_x, text_y))
    
    def render_possibilities(self, cell: Cell, screen_x: int, screen_y: int):
        """Render small indicators for each possibility in a cell."""
        if cell.collapsed or not cell.possibilities:
            return
        
        possibilities = list(cell.possibilities)
        num_possibilities = len(possibilities)
        
        # Calculate grid layout for possibilities
        cols = min(3, num_possibilities)  # Max 3 columns
        rows = (num_possibilities + cols - 1) // cols  # Ceiling division
        
        sub_size = self.tile_size // max(cols, rows, 2)
        start_x = screen_x + (self.tile_size - cols * sub_size) // 2
        start_y = screen_y + (self.tile_size - rows * sub_size) // 2
        
        for i, tile_type in enumerate(possibilities):
            row = i // cols
            col = i % cols
            
            sub_x = start_x + col * sub_size
            sub_y = start_y + row * sub_size
            sub_rect = pygame.Rect(sub_x, sub_y, sub_size, sub_size)
            
            color = self.tileset.get_tile(tile_type).color
            pygame.draw.rect(self.screen, color, sub_rect)
    
    def render_legend(self, x: int, y: int, tile_size: int = 30, spacing: int = 5):
        """Render a legend showing all tile types."""
        legend_y = y
        
        for tile_type in self.tileset.get_all_types():
            tile = self.tileset.get_tile(tile_type)
            
            # Draw tile color
            rect = pygame.Rect(x, legend_y, tile_size, tile_size)
            pygame.draw.rect(self.screen, tile.color, rect)
            pygame.draw.rect(self.screen, self.colors['border'], rect, 2)
            
            # Draw tile name
            text_surface = self.font.render(tile.name, True, self.colors['text'])
            text_x = x + tile_size + 10
            text_y = legend_y + (tile_size - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
            
            legend_y += tile_size + spacing
    
    def render_statistics(self, wfc: WaveFunctionCollapse, x: int, y: int):
        """Render generation statistics."""
        stats = wfc.get_statistics()
        
        lines = [
            f"Step: {stats['generation_step']}",
            f"Collapsed: {stats['collapsed_cells']}/{stats['total_cells']}",
            f"Progress: {stats['completion_percentage']:.1f}%",
            f"Uncollapsed: {stats['uncollapsed_cells']}",
        ]
        
        # Add entropy distribution if there are uncollapsed cells
        if stats['entropy_distribution']:
            lines.append("Entropy distribution:")
            for entropy, count in sorted(stats['entropy_distribution'].items()):
                lines.append(f"  {entropy}: {count} cells")
        
        current_y = y
        for line in lines:
            text_surface = self.font.render(line, True, self.colors['text'])
            self.screen.blit(text_surface, (x, current_y))
            current_y += text_surface.get_height() + 2
    
    def get_cell_at_pixel(self, wfc: WaveFunctionCollapse, 
                         pixel_x: int, pixel_y: int) -> Optional[Cell]:
        """Get the cell at a given pixel coordinate."""
        # Adjust for offset
        grid_x = (pixel_x - self.offset_x) // self.tile_size
        grid_y = (pixel_y - self.offset_y) // self.tile_size
        
        if 0 <= grid_x < wfc.width and 0 <= grid_y < wfc.height:
            return wfc.grid[grid_y][grid_x]
        
        return None
    
    def highlight_cell(self, cell: Cell, color: Tuple[int, int, int] = (255, 255, 0)):
        """Highlight a specific cell with a colored border."""
        screen_x = self.offset_x + cell.x * self.tile_size
        screen_y = self.offset_y + cell.y * self.tile_size
        
        rect = pygame.Rect(screen_x, screen_y, self.tile_size, self.tile_size)
        pygame.draw.rect(self.screen, color, rect, 3)
    
    def render_grid_lines(self, wfc: WaveFunctionCollapse, 
                         color: Tuple[int, int, int] = None):
        """Render grid lines over the entire grid."""
        if color is None:
            color = self.colors['border']
        
        # Vertical lines
        for x in range(wfc.width + 1):
            start_x = self.offset_x + x * self.tile_size
            start_y = self.offset_y
            end_y = self.offset_y + wfc.height * self.tile_size
            pygame.draw.line(self.screen, color, (start_x, start_y), (start_x, end_y))
        
        # Horizontal lines
        for y in range(wfc.height + 1):
            start_y = self.offset_y + y * self.tile_size
            start_x = self.offset_x
            end_x = self.offset_x + wfc.width * self.tile_size
            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, start_y))
