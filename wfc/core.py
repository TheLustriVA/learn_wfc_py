"""Core Wave Function Collapse algorithm implementation."""

import random
from typing import List, Set, Optional, Tuple, Dict
from dataclasses import dataclass, field
from collections import deque
from .tiles import TileSet, TileType


@dataclass
class Cell:
    """Represents a single cell in the WFC grid."""
    x: int
    y: int
    possibilities: Set[TileType] = field(default_factory=set)
    collapsed: bool = False
    
    @property
    def entropy(self) -> int:
        """Return the entropy (number of possibilities) for this cell."""
        return len(self.possibilities) if not self.collapsed else 0
    
    def collapse_to(self, tile_type: TileType) -> bool:
        """Collapse this cell to a specific tile type."""
        if tile_type not in self.possibilities:
            return False
        
        self.possibilities = {tile_type}
        self.collapsed = True
        return True
    
    def remove_possibility(self, tile_type: TileType) -> bool:
        """Remove a possibility from this cell. Returns True if possibilities changed."""
        if tile_type in self.possibilities:
            self.possibilities.discard(tile_type)
            return True
        return False
    
    def __str__(self):
        if self.collapsed:
            tile_type = next(iter(self.possibilities))
            return f"[{tile_type.value[0].upper()}]"
        else:
            return f"({self.entropy})"


class WaveFunctionCollapse:
    """Main Wave Function Collapse algorithm implementation."""
    
    def __init__(self, width: int, height: int, tileset: TileSet, seed: Optional[int] = None):
        self.width = width
        self.height = height
        self.tileset = tileset
        self.grid: List[List[Cell]] = []
        self.generation_step = 0
        self.max_retries = 10
        
        if seed is not None:
            random.seed(seed)
        
        # Validate tileset before starting
        if not self.tileset.validate_constraints():
            raise ValueError("Invalid tileset constraints")
        
        self.initialize_grid()
    
    def initialize_grid(self):
        """Initialize all cells with all possible tile types."""
        all_types = self.tileset.get_all_types()
        
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y, all_types.copy())
                row.append(cell)
            self.grid.append(row)
        
        self.generation_step = 0
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Get cell at coordinates, return None if out of bounds."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get valid neighbor coordinates (4-directional)."""
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
    
    def find_min_entropy_cells(self) -> List[Cell]:
        """Find all uncollapsed cells with minimum entropy > 0."""
        min_entropy = float('inf')
        candidates = []
        
        for row in self.grid:
            for cell in row:
                if not cell.collapsed and cell.entropy > 0:
                    if cell.entropy < min_entropy:
                        min_entropy = cell.entropy
                        candidates = [cell]
                    elif cell.entropy == min_entropy:
                        candidates.append(cell)
        
        return candidates
    
    def collapse_cell(self, cell: Cell) -> bool:
        """Collapse a cell to a single possibility."""
        if not cell.possibilities:
            return False  # Contradiction - no valid possibilities
        
        if cell.collapsed:
            return True  # Already collapsed
        
        # Choose weighted random tile (could implement tile weights here)
        chosen_type = random.choice(list(cell.possibilities))
        return cell.collapse_to(chosen_type)
    
    def propagate_constraints(self, start_x: int, start_y: int) -> bool:
        """Propagate constraints using breadth-first search."""
        queue = deque([(start_x, start_y)])
        visited = set()
        
        while queue:
            x, y = queue.popleft()
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            current_cell = self.get_cell(x, y)
            if not current_cell:
                continue
            
            # Get all neighbors and update their possibilities
            for nx, ny in self.get_neighbors(x, y):
                neighbor = self.get_cell(nx, ny)
                if not neighbor or neighbor.collapsed:
                    continue
                
                # Calculate valid possibilities for neighbor based on current cell
                valid_for_neighbor = set()
                
                if current_cell.collapsed:
                    # Current cell has one tile type
                    current_type = next(iter(current_cell.possibilities))
                    valid_for_neighbor = self.tileset.get_valid_neighbors(current_type)
                else:
                    # Current cell has multiple possibilities
                    for possible_type in current_cell.possibilities:
                        valid_for_neighbor.update(self.tileset.get_valid_neighbors(possible_type))
                
                # Remove invalid possibilities from neighbor
                old_possibilities = neighbor.possibilities.copy()
                neighbor.possibilities &= valid_for_neighbor
                
                # Check for contradiction
                if not neighbor.possibilities:
                    return False
                
                # If neighbor's possibilities changed, add it to queue
                if neighbor.possibilities != old_possibilities:
                    queue.append((nx, ny))
        
        return True
    
    def is_complete(self) -> bool:
        """Check if all cells are collapsed."""
        for row in self.grid:
            for cell in row:
                if not cell.collapsed:
                    return False
        return True
    
    def has_contradiction(self) -> bool:
        """Check if any uncollapsed cell has no possibilities."""
        for row in self.grid:
            for cell in row:
                if not cell.collapsed and not cell.possibilities:
                    return True
        return False
    
    def generate_step(self) -> Tuple[bool, str]:
        """Perform one step of WFC generation. Returns (continue, status_message)."""
        self.generation_step += 1
        
        # Check for contradictions
        if self.has_contradiction():
            return False, f"Step {self.generation_step}: Contradiction detected"
        
        # Check if complete
        if self.is_complete():
            return False, f"Step {self.generation_step}: Generation complete!"
        
        # Find cells with minimum entropy
        candidates = self.find_min_entropy_cells()
        if not candidates:
            return False, f"Step {self.generation_step}: No valid cells to collapse"
        
        # Choose a cell to collapse
        chosen_cell = random.choice(candidates)
        
        # Collapse the cell
        if not self.collapse_cell(chosen_cell):
            return False, f"Step {self.generation_step}: Failed to collapse cell at ({chosen_cell.x}, {chosen_cell.y})"
        
        # Propagate constraints
        if not self.propagate_constraints(chosen_cell.x, chosen_cell.y):
            return False, f"Step {self.generation_step}: Constraint propagation failed"
        
        return True, f"Step {self.generation_step}: Collapsed cell at ({chosen_cell.x}, {chosen_cell.y})"
    
    def generate(self, max_steps: int = 10000) -> bool:
        """Generate the complete map. Returns True if successful."""
        for attempt in range(self.max_retries):
            self.initialize_grid()
            
            for step in range(max_steps):
                continue_generation, message = self.generate_step()
                
                if not continue_generation:
                    if self.is_complete():
                        print(f"Generation successful on attempt {attempt + 1}: {message}")
                        return True
                    else:
                        print(f"Attempt {attempt + 1} failed: {message}")
                        break
            
            print(f"Attempt {attempt + 1} exceeded max steps ({max_steps})")
        
        print(f"Generation failed after {self.max_retries} attempts")
        return False
    
    def get_tile_at(self, x: int, y: int) -> Optional[TileType]:
        """Get the collapsed tile type at position."""
        cell = self.get_cell(x, y)
        if cell and cell.collapsed:
            return next(iter(cell.possibilities))
        return None
    
    def print_grid(self, show_entropy: bool = False):
        """Print a text representation of the grid."""
        print(f"\nGrid state (Step {self.generation_step}):")
        for row in self.grid:
            line = ""
            for cell in row:
                if show_entropy and not cell.collapsed:
                    line += f"{cell.entropy:2d} "
                else:
                    if cell.collapsed:
                        tile_type = next(iter(cell.possibilities))
                        line += f"{tile_type.value[0].upper():2s} "
                    else:
                        line += "?? "
            print(line)
    
    def get_statistics(self) -> Dict[str, any]:
        """Get generation statistics."""
        total_cells = self.width * self.height
        collapsed_cells = sum(1 for row in self.grid for cell in row if cell.collapsed)
        
        entropy_distribution = {}
        for row in self.grid:
            for cell in row:
                if not cell.collapsed:
                    entropy = cell.entropy
                    entropy_distribution[entropy] = entropy_distribution.get(entropy, 0) + 1
        
        return {
            'total_cells': total_cells,
            'collapsed_cells': collapsed_cells,
            'uncollapsed_cells': total_cells - collapsed_cells,
            'completion_percentage': (collapsed_cells / total_cells) * 100,
            'entropy_distribution': entropy_distribution,
            'generation_step': self.generation_step,
        }
