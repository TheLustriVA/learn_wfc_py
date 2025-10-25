"""Tile system for Wave Function Collapse."""

from enum import Enum
from dataclasses import dataclass
from typing import Set, Dict


class TileType(Enum):
    """Available tile types for map generation."""
    GRASS = "grass"
    WATER = "water"
    SAND = "sand"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    STONE = "stone"
    SNOW = "snow"


@dataclass
class Tile:
    """Represents a single tile with its properties."""
    tile_type: TileType
    color: tuple  # RGB color for rendering
    name: str = ""
    
    def __post_init__(self):
        if not self.name:
            self.name = self.tile_type.value.title()
    
    def __hash__(self):
        return hash(self.tile_type)
    
    def __str__(self):
        return f"{self.name} ({self.tile_type.value})"


class TileSet:
    """Manages tiles and their adjacency constraints."""
    
    def __init__(self):
        # Define all available tiles with colors
        self.tiles = {
            TileType.GRASS: Tile(TileType.GRASS, (34, 139, 34)),      # Forest green
            TileType.WATER: Tile(TileType.WATER, (0, 100, 200)),      # Deep blue
            TileType.SAND: Tile(TileType.SAND, (238, 203, 173)),      # Light tan
            TileType.FOREST: Tile(TileType.FOREST, (0, 100, 0)),      # Dark green
            TileType.MOUNTAIN: Tile(TileType.MOUNTAIN, (139, 137, 137)), # Gray
            TileType.STONE: Tile(TileType.STONE, (105, 105, 105)),     # Dark gray
            TileType.SNOW: Tile(TileType.SNOW, (255, 250, 250)),       # Snow white
        }
        
        # Define adjacency constraints - which tiles can be next to each other
        self.constraints = {
            TileType.GRASS: {
                TileType.GRASS, TileType.FOREST, TileType.MOUNTAIN, 
                TileType.SAND, TileType.STONE
            },
            TileType.WATER: {
                TileType.WATER, TileType.SAND
            },
            TileType.SAND: {
                TileType.SAND, TileType.WATER, TileType.GRASS, TileType.STONE
            },
            TileType.FOREST: {
                TileType.FOREST, TileType.GRASS, TileType.MOUNTAIN, TileType.STONE
            },
            TileType.MOUNTAIN: {
                TileType.MOUNTAIN, TileType.GRASS, TileType.FOREST, 
                TileType.STONE, TileType.SNOW
            },
            TileType.STONE: {
                TileType.STONE, TileType.MOUNTAIN, TileType.GRASS, 
                TileType.FOREST, TileType.SAND
            },
            TileType.SNOW: {
                TileType.SNOW, TileType.MOUNTAIN, TileType.STONE
            },
        }
    
    def get_tile(self, tile_type: TileType) -> Tile:
        """Get tile object by type."""
        return self.tiles[tile_type]
    
    def get_valid_neighbors(self, tile_type: TileType) -> Set[TileType]:
        """Get all valid neighboring tile types for a given tile."""
        return self.constraints.get(tile_type, set())
    
    def can_be_adjacent(self, tile1: TileType, tile2: TileType) -> bool:
        """Check if two tile types can be adjacent."""
        return tile2 in self.constraints.get(tile1, set())
    
    def get_all_types(self) -> Set[TileType]:
        """Get all available tile types."""
        return set(self.tiles.keys())
    
    def validate_constraints(self) -> bool:
        """Validate that all constraints are symmetric and complete."""
        for tile_type, neighbors in self.constraints.items():
            for neighbor in neighbors:
                # Check if relationship is symmetric
                if tile_type not in self.constraints.get(neighbor, set()):
                    print(f"Warning: Asymmetric constraint between {tile_type} and {neighbor}")
                    return False
                    
                # Check if neighbor tile exists
                if neighbor not in self.tiles:
                    print(f"Error: Constraint references non-existent tile {neighbor}")
                    return False
        
        return True


# Predefined tile sets for different environments
class BiomeTileSet(TileSet):
    """Extended tileset with biome-specific configurations."""
    
    @classmethod
    def create_ocean_biome(cls):
        """Create a tileset focused on ocean/coastal areas."""
        tileset = cls()
        # Override constraints for ocean biome
        tileset.constraints = {
            TileType.WATER: {TileType.WATER, TileType.SAND},
            TileType.SAND: {TileType.SAND, TileType.WATER, TileType.GRASS},
            TileType.GRASS: {TileType.GRASS, TileType.SAND, TileType.FOREST},
            TileType.FOREST: {TileType.FOREST, TileType.GRASS},
        }
        return tileset
    
    @classmethod
    def create_mountain_biome(cls):
        """Create a tileset focused on mountainous terrain."""
        tileset = cls()
        # Override constraints for mountain biome
        tileset.constraints = {
            TileType.GRASS: {TileType.GRASS, TileType.FOREST, TileType.STONE},
            TileType.FOREST: {TileType.FOREST, TileType.GRASS, TileType.MOUNTAIN},
            TileType.MOUNTAIN: {TileType.MOUNTAIN, TileType.FOREST, TileType.STONE, TileType.SNOW},
            TileType.STONE: {TileType.STONE, TileType.MOUNTAIN, TileType.GRASS},
            TileType.SNOW: {TileType.SNOW, TileType.MOUNTAIN},
        }
        return tileset
