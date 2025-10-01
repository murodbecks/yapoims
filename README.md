# yapoims

**Project for Individual Assignment at AI1030 - Python Programming, MBZUAI**

**Yet another POI Management System** (`yapoims` for short) - is a POI (Point of Interest) Management System built in Python. The project is done as part of `Individual Assignment 1` in `AI1030 - Python Programming` course at MBZUAI.

More information about project requirements can be found in [the assignment brief](files/IA1_Brief.pdf). The report on `Design & Data Model`, `Edge Policies`, and `Usage Policy` can be found in [the report](files/report.md). The reflection on `trade-offs and constraints that shaped the design` can be found in [the reflection](files/reflection.md). Also, [AI Usage log](files/AI_Usage_Log.csv) where I documented my prompts when building the projects is available.

## Features

### Core Functionality
- **POI Management**: Create, delete, and manage Points of Interest with custom attributes
- **POI Types**: Dynamic POI type system with customizable attributes
- **Visitor Tracking**: Track visitors and their visits to POIs with ratings and dates
- **Geospatial Queries**: Distance-based searches, nearest neighbors, boundary detection
- **Analytics**: Coverage analysis, popularity metrics, visitor patterns

### Key Capabilities
- **1000×1000 coordinate grid** with floating-point precision
- **YAML configuration loading** with validation and error handling
- **Euclidean distance calculations** with epsilon-based boundary detection
- **Immutable POI identifiers** - IDs are never reused after deletion
- **Type safety** - POI types can only be deleted if no POIs use them
- **Visit tracking** with date validation (dd/mm/yyyy format) and optional ratings (1-10)
- **Interactive CLI** with comprehensive menu system
- **Python API** for programmatic access

## Setup and Installation

To run the POI management system, you need Python 3.6+ and `pip`.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/murodbecks/yapoims.git
   cd yapoims/
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the project in editable mode:**
   This command installs any dependencies and makes the `yapoims` command available in your terminal.
   ```bash
   pip install -e .
   ```

## Usage

### CLI Usage

The system provides an interactive command-line interface with comprehensive menu navigation:

```bash
# Run with no data (empty system)
yapoims

# Load sample configuration
yapoims --demo

# Load custom configuration file
yapoims --config path/to/your/config.yaml
```

#### CLI Menu Structure
```
Main Menu
├── POI Management
│   ├── Add/Delete POI Types
│   ├── Add/Delete POIs
│   ├── Rename POI Types
│   └── Manage Type Attributes
├── Visitor Management
│   ├── Add Visitors
│   ├── Record Visits
│   └── View Visitor Details
├── POI Queries
│   ├── Find Nearest POI Pair
│   ├── POIs Within Radius
│   ├── K Closest POIs
│   └── Boundary Detection
├── Analytics
│   ├── Most Popular POIs
│   ├── Most Active Visitors
│   └── Coverage Fairness
└── System Information
```

### Python API Usage

You can also use yapoims programmatically in your Python code:

```python
from yapoims import PoiManagementSystem

# Initialize system
system = PoiManagementSystem()

# Or load from configuration
system = PoiManagementSystem('configs/sample.yaml')

# Add POI types
system.add_poi_type('restaurant', ['cuisine', 'price_range', 'rating'])
system.add_poi_type('museum', ['opening_hours', 'entrance_fee', 'exhibits'])

# Add POIs
system.add_poi('Central Restaurant', 'restaurant', 500, 300, {
    'cuisine': 'Italian', 
    'price_range': 'mid-range',
    'rating': 4.5
})

system.add_poi('Art Museum', 'museum', 200, 700, {
    'opening_hours': '9:00-17:00',
    'entrance_fee': '10 USD',
    'exhibits': 'Modern Art'
})

# Add visitors and visits
system.add_visitor('John Doe', 'American', [
    {'poi_name': 'Central Restaurant', 'date': '15/10/2024', 'rating': 8},
    {'poi_name': 'Art Museum', 'date': '16/10/2024', 'rating': 9}
])

# Query POIs by location
nearby_pois = system.get_pois_within_distance(500, 300, radius=100)
print(f"Found {len(nearby_pois)} POIs within 100 units")

# Find closest POIs
closest_pois = system.get_k_closest_pois(400, 400, k=3)
for poi_id, name, coords, poi_type, distance in closest_pois:
    print(f"{name} ({poi_type}) - {distance:.1f} units away")

# Analytics queries
popular_pois = system.get_crowdest_k_pois(k=5)
active_visitors = system.get_most_visited_k_visitors(k=3)

# Coverage fairness analysis
special_visitors = system.get_special_visitors(m=2, t=2)  # ≥2 POIs, ≥2 types
```

## Architecture

### Core Classes

#### `Poi` Class
Represents a Point of Interest with immutable core properties:
- **Immutable**: ID, name, coordinates (x, y)
- **Mutable**: POI type, custom attributes
- **Validation**: Coordinates must be within 1000×1000 grid

#### `Visitor` Class
Represents a visitor with visit history:
- **Immutable**: ID, name, nationality
- **Mutable**: Visit records
- **Validation**: Date format (dd/mm/yyyy), ratings (1-10)

#### `PoiManagementSystem` Class
Main system orchestrator:
- **POI Management**: CRUD operations with type constraints
- **Visitor Management**: Visit tracking and analytics
- **Geospatial Queries**: Distance calculations with epsilon handling
- **Data Integrity**: ID uniqueness, referential consistency

### Key Design Decisions

1. **Immutable IDs**: Once a POI or visitor is deleted, their ID is never reused
2. **Type Safety**: POI types can only be deleted if no POIs use them
3. **Coordinate System**: 1000×1000 grid with floating-point precision
4. **Distance Calculation**: Euclidean distance with configurable epsilon for boundary detection
5. **Date Format**: Strict dd/mm/yyyy validation for visit dates

### Geospatial Queries

```python
# Find POIs within radius
nearby = system.get_pois_within_distance(x=500, y=500, r=100)

# Get K closest POIs
closest = system.get_k_closest_pois(x=400, y=300, k=5)

# Boundary detection with epsilon
boundary = system.get_pois_in_boundary(x=500, y=500, r=100.0, epsilon=1e-6)

# Find nearest POI pair in entire system
nearest_pair = system.get_nearest_pois()
```


## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_poi.py -v

# Run with coverage
python -m pytest tests/ --cov=yapoims --cov-report=html
```

The test suite includes:
- **Unit tests** for all core classes
- **Integration tests** for system workflows
- **Edge case testing** for boundary conditions
- **Data validation tests** for configuration loading

## Requirements

- **Python**: 3.6 or higher
- **Dependencies**: 
  - `pytz==2025.2` (timezone handling)
  - `pytest==8.4.2` (testing framework)

No external dependencies for core functionality - uses only Python standard library for maximum compatibility.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Author

**Abror Shopulatov** - MBZUAI Student  
Course: AI1030 - Python Programming  
Assignment: Individual Assignment 1 - POI Management System