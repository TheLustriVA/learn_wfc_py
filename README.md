# Wave Function Collapse - Python Learning Implementation

> A comprehensive, educational implementation of Wave Function Collapse (WFC) for procedural map generation using Python 3.12 and Pygame.

## 🎯 What is Wave Function Collapse?

Wave Function Collapse is a procedural generation algorithm inspired by quantum mechanics that creates coherent, rule-based content. It works by:

1. **Superposition**: Each cell starts with all possible tile types
2. **Observation**: Cells are "collapsed" to single definite states
3. **Constraint Propagation**: Neighboring cells update their possibilities based on adjacency rules
4. **Iteration**: Process continues until all cells are determined or a contradiction occurs

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/TheLustriVA/learn_wfc_py.git
cd learn_wfc_py

# Run the interactive demo
python main.py
```

### Requirements
- Python 3.12+
- Pygame 2.6+

Dependencies are managed with `uv` - see `pyproject.toml` for details.

## 🎮 Interactive Controls

| Key | Action |
|-----|--------|
| **Space** | Step through generation one cell at a time |
| **G** | Generate a complete new map instantly |
| **E** | Toggle entropy visualization |
| **A** | Toggle auto-step mode |
| **Q** | Quit application |
| **Mouse Click** | Inspect individual cell states |

## 📁 Project Structure

```
learn_wfc_py/
├── main.py              # Interactive Pygame demo
├── wfc/                 # Core WFC implementation
│   ├── __init__.py      # Package initialization
│   ├── core.py          # Main WFC algorithm
│   ├── tiles.py         # Tile definitions and constraints
│   └── renderer.py      # Pygame visualization
├── pyproject.toml       # Python dependencies
└── README.md           # This file
```

## 🧩 Core Components

### Tiles System (`wfc/tiles.py`)

Defines tile types and their adjacency constraints:

```python
from wfc import TileSet, TileType

# Create a tileset with predefined biome tiles
tileset = TileSet()

# Check which tiles can be adjacent
can_connect = tileset.can_be_adjacent(TileType.WATER, TileType.SAND)
print(f"Water can connect to sand: {can_connect}")  # True
```

### WFC Algorithm (`wfc/core.py`)

Main generation logic with step-by-step control:

```python
from wfc import WaveFunctionCollapse

# Create a 20x15 grid
wfc = WaveFunctionCollapse(width=20, height=15, tileset=tileset)

# Generate complete map
if wfc.generate():
    print("Generation successful!")
    
# Or step through manually
while not wfc.is_complete():
    continue_generation, message = wfc.generate_step()
    print(message)
    if not continue_generation:
        break
```

### Visualization (`wfc/renderer.py`)

Pygame rendering with debugging features:

```python
from wfc import WFCRenderer

renderer = WFCRenderer(screen, tileset, tile_size=20)

# Render the grid with entropy visualization
renderer.render_grid(wfc, show_entropy=True)

# Show generation statistics
renderer.render_statistics(wfc, x=100, y=100)
```

## 🎨 Customizing Tiles and Constraints

### Creating Custom Tiles

```python
from enum import Enum
from wfc import Tile, TileSet

# Define new tile types
class MyTileType(Enum):
    LAVA = "lava"
    ICE = "ice"
    CRYSTAL = "crystal"

# Create custom tileset
class MyTileSet(TileSet):
    def __init__(self):
        super().__init__()
        
        # Add custom tiles
        self.tiles.update({
            MyTileType.LAVA: Tile(MyTileType.LAVA, (255, 100, 0)),  # Orange
            MyTileType.ICE: Tile(MyTileType.ICE, (100, 200, 255)),   # Light blue
            MyTileType.CRYSTAL: Tile(MyTileType.CRYSTAL, (255, 0, 255)), # Magenta
        })
        
        # Define adjacency rules
        self.constraints.update({
            MyTileType.LAVA: {MyTileType.LAVA, TileType.STONE},
            MyTileType.ICE: {MyTileType.ICE, TileType.WATER, TileType.SNOW},
            MyTileType.CRYSTAL: {MyTileType.CRYSTAL, TileType.MOUNTAIN, TileType.STONE},
        })
```

### Biome Presets

The implementation includes specialized biome configurations:

```python
from wfc import BiomeTileSet

# Ocean-focused generation
ocean_tileset = BiomeTileSet.create_ocean_biome()

# Mountain-focused generation  
mountain_tileset = BiomeTileSet.create_mountain_biome()
```

## 🔧 Advanced Features

### Generation Statistics

```python
stats = wfc.get_statistics()
print(f"Completion: {stats['completion_percentage']:.1f}%")
print(f"Entropy distribution: {stats['entropy_distribution']}")
```

### Debugging Tools

```python
# Print text representation of grid
wfc.print_grid(show_entropy=True)

# Check for contradictions
if wfc.has_contradiction():
    print("Generation failed - contradiction detected")

# Inspect individual cells
cell = wfc.get_cell(x=5, y=3)
print(f"Cell entropy: {cell.entropy}")
print(f"Possible tiles: {[t.value for t in cell.possibilities]}")
```

### Performance Configuration

```python
# Control generation parameters
wfc = WaveFunctionCollapse(
    width=100, 
    height=100, 
    tileset=tileset,
    seed=42  # For reproducible results
)

# Set retry behavior
wfc.max_retries = 5

# Generate with step limit
success = wfc.generate(max_steps=10000)
```

## 🎯 Learning Exercises

### Beginner
1. **Modify tile colors** in the TileSet class
2. **Experiment with constraints** - make water only adjacent to sand
3. **Try different grid sizes** and observe performance changes

### Intermediate
4. **Add weighted tile selection** for biome preferences
5. **Implement simple backtracking** when contradictions occur
6. **Create a custom biome** with your own tile types

### Advanced
7. **Multi-scale generation** - generate coarse then refine
8. **Conditional constraints** based on neighboring patterns
9. **Performance optimization** for large grids

## 📚 Learning Resources

For comprehensive learning materials, visit the **[Notion Learning Hub](https://www.notion.so/297e02c2f852813e9363dfea2c6e8813)** which includes:

- **Theory & Concepts** - Understanding WFC fundamentals
- **Implementation Guide** - Step-by-step coding tutorial  
- **Code Examples** - Working implementations and exercises
- **Advanced Techniques** - Optimization and extensions
- **Resources & References** - Papers, tutorials, and further reading

## 🎮 Example Applications

This WFC implementation can be extended for:

- **Roguelike dungeons** - Room and corridor generation
- **City planning** - District and road layout
- **Terrain generation** - Realistic landscape creation
- **Texture synthesis** - Seamless pattern generation
- **Level design** - Puzzle and platformer layouts

## 🤝 Contributing

This is an educational project! Contributions welcome:

1. **Bug fixes** and optimizations
2. **New tile sets** and biome examples
3. **Advanced algorithm variants**
4. **Documentation improvements**
5. **Performance benchmarks**

## 📖 Further Reading

- [Original WFC by Maxim Gumin](https://github.com/mxgmn/WaveFunctionCollapse)
- ["Wave Function Collapse Explained" by Robert Heaton](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/)
- [Procedural Content Generation research papers](https://pcgbook.com/)

## 📄 License

MIT License - see `LICENSE` file for details.

---

**Ready to generate infinite worlds? Run `python main.py` and start exploring!** 🚀
