#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────────────
#  Wave Function Collapse Demo with Pygame
#  Python 3.12 + Pygame 2.6+ + Custom WFC Implementation
# ──────────────────────────────────────────────────────────────────────

import pygame
import sys
from wfc import WaveFunctionCollapse, TileSet, WFCRenderer, BiomeTileSet

# ----------------------------------------------------------------------
#  Configuration
# ----------------------------------------------------------------------
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
MENU_HEIGHT = 40

# WFC Configuration
GRID_WIDTH = 60
GRID_HEIGHT = 40
TILE_SIZE = 15
GRID_OFFSET_X = 10
GRID_OFFSET_Y = MENU_HEIGHT + 10

# UI Configuration
LEGEND_X = GRID_OFFSET_X + GRID_WIDTH * TILE_SIZE + 20
STATS_X = LEGEND_X
STATS_Y = 400

# ----------------------------------------------------------------------
#  Initialize Pygame
# ----------------------------------------------------------------------
pygame.init()
pygame.display.set_caption('Wave Function Collapse - Procedural Map Generator')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# ----------------------------------------------------------------------
#  Colors and Fonts
# ----------------------------------------------------------------------
COLORS = {
    'background': (20, 20, 30),
    'menu_bg': (40, 40, 50),
    'button_bg': (60, 120, 200),
    'button_hover': (80, 140, 220),
    'text': (255, 255, 255),
    'border': (100, 100, 100),
}

font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)

# ----------------------------------------------------------------------
#  Button Class
# ----------------------------------------------------------------------
class Button:
    def __init__(self, x, y, width, height, text, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()
    
    def draw(self, screen):
        color = COLORS['button_hover'] if self.hovered else COLORS['button_bg']
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS['border'], self.rect, 2)
        
        text_surface = font.render(self.text, True, COLORS['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# ----------------------------------------------------------------------
#  WFC Demo Application
# ----------------------------------------------------------------------
class WFCDemo:
    def __init__(self):
        # Initialize WFC components
        self.tileset = TileSet()
        self.wfc = None
        self.renderer = WFCRenderer(
            screen, self.tileset, TILE_SIZE, 
            (GRID_OFFSET_X, GRID_OFFSET_Y)
        )
        
        # UI state
        self.show_entropy = False
        self.show_legend = True
        self.show_stats = True
        self.auto_step = False
        self.step_delay = 100  # milliseconds
        self.last_step_time = 0
        
        # Create buttons
        button_y = 5
        button_spacing = 120
        
        self.buttons = [
            Button(10, button_y, 100, 30, "Generate", self.generate_map),
            Button(10 + button_spacing, button_y, 100, 30, "Step", self.step_generation),
            Button(10 + button_spacing * 2, button_y, 100, 30, "Auto Step", self.toggle_auto_step),
            Button(10 + button_spacing * 3, button_y, 100, 30, "Show Entropy", self.toggle_entropy),
            Button(10 + button_spacing * 4, button_y, 100, 30, "Ocean Biome", self.set_ocean_biome),
            Button(10 + button_spacing * 5, button_y, 100, 30, "Mountain Biome", self.set_mountain_biome),
            Button(SCREEN_WIDTH - 110, button_y, 100, 30, "Quit", self.quit_app),
        ]
        
        # Generate initial map
        self.generate_map()
    
    def generate_map(self):
        """Generate a new complete map."""
        print("Generating new map...")
        self.wfc = WaveFunctionCollapse(GRID_WIDTH, GRID_HEIGHT, self.tileset, seed=None)
        success = self.wfc.generate()
        
        if success:
            print("Map generation successful!")
        else:
            print("Map generation failed, retrying...")
            self.generate_map()  # Retry
    
    def step_generation(self):
        """Perform one step of WFC generation."""
        if not self.wfc:
            self.wfc = WaveFunctionCollapse(GRID_WIDTH, GRID_HEIGHT, self.tileset)
        
        if not self.wfc.is_complete():
            continue_generation, message = self.wfc.generate_step()
            print(message)
            
            if not continue_generation and not self.wfc.is_complete():
                print("Generation failed, starting over...")
                self.wfc = WaveFunctionCollapse(GRID_WIDTH, GRID_HEIGHT, self.tileset)
    
    def toggle_auto_step(self):
        """Toggle automatic stepping."""
        self.auto_step = not self.auto_step
        self.buttons[2].text = "Stop Auto" if self.auto_step else "Auto Step"
        print(f"Auto step: {'ON' if self.auto_step else 'OFF'}")
    
    def toggle_entropy(self):
        """Toggle entropy display."""
        self.show_entropy = not self.show_entropy
        self.buttons[3].text = "Hide Entropy" if self.show_entropy else "Show Entropy"
        print(f"Entropy display: {'ON' if self.show_entropy else 'OFF'}")
    
    def set_ocean_biome(self):
        """Switch to ocean biome tileset."""
        self.tileset = BiomeTileSet.create_ocean_biome()
        self.renderer.tileset = self.tileset
        print("Switched to ocean biome")
        self.generate_map()
    
    def set_mountain_biome(self):
        """Switch to mountain biome tileset."""
        self.tileset = BiomeTileSet.create_mountain_biome()
        self.renderer.tileset = self.tileset
        print("Switched to mountain biome")
        self.generate_map()
    
    def quit_app(self):
        """Quit the application."""
        pygame.quit()
        sys.exit()
    
    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.QUIT:
            self.quit_app()
        
        # Handle button events
        for button in self.buttons:
            button.handle_event(event)
        
        # Handle keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.step_generation()
            elif event.key == pygame.K_g:
                self.generate_map()
            elif event.key == pygame.K_e:
                self.toggle_entropy()
            elif event.key == pygame.K_a:
                self.toggle_auto_step()
            elif event.key == pygame.K_q:
                self.quit_app()
        
        # Handle mouse clicks on grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.wfc:
                cell = self.renderer.get_cell_at_pixel(self.wfc, event.pos[0], event.pos[1])
                if cell:
                    print(f"Clicked cell ({cell.x}, {cell.y}): "
                          f"Collapsed={cell.collapsed}, Entropy={cell.entropy}, "
                          f"Possibilities={[t.value for t in cell.possibilities]}")
    
    def update(self):
        """Update the application state."""
        current_time = pygame.time.get_ticks()
        
        # Auto-stepping
        if (self.auto_step and self.wfc and not self.wfc.is_complete() and
            current_time - self.last_step_time > self.step_delay):
            self.step_generation()
            self.last_step_time = current_time
    
    def draw(self):
        """Draw the application."""
        # Clear screen
        screen.fill(COLORS['background'])
        
        # Draw menu background
        menu_rect = pygame.Rect(0, 0, SCREEN_WIDTH, MENU_HEIGHT)
        pygame.draw.rect(screen, COLORS['menu_bg'], menu_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(screen)
        
        # Draw WFC grid
        if self.wfc:
            self.renderer.render_grid(self.wfc, show_entropy=self.show_entropy)
        
        # Draw legend
        if self.show_legend:
            legend_title = font.render("Tile Legend:", True, COLORS['text'])
            screen.blit(legend_title, (LEGEND_X, GRID_OFFSET_Y))
            self.renderer.render_legend(LEGEND_X, GRID_OFFSET_Y + 30)
        
        # Draw statistics
        if self.show_stats and self.wfc:
            stats_title = font.render("Generation Stats:", True, COLORS['text'])
            screen.blit(stats_title, (STATS_X, STATS_Y))
            self.renderer.render_statistics(self.wfc, STATS_X, STATS_Y + 30)
        
        # Draw help text
        help_text = [
            "Controls:",
            "Space: Step generation",
            "G: Generate new map",
            "E: Toggle entropy display",
            "A: Toggle auto-stepping",
            "Q: Quit",
            "Click on cells for info",
        ]
        
        help_y = STATS_Y + 200
        for line in help_text:
            text_surface = small_font.render(line, True, COLORS['text'])
            screen.blit(text_surface, (STATS_X, help_y))
            help_y += text_surface.get_height() + 2
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main application loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                self.handle_event(event)
            
            # Update
            self.update()
            
            # Draw
            self.draw()
            
            # Control frame rate
            clock.tick(FPS)

# ----------------------------------------------------------------------
#  Main Entry Point
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        app = WFCDemo()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()
