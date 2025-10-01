# Report: YAPOIMS - Yet Another POI Management System

## 1. Design & Data Model

The system is designed around a modular, in-memory architecture with three core entities. It loads an initial state from a configuration file but does not persist changes back to disk, treating each session as a distinct instance.

### Entities

1.  **`Poi` Class (`poi.py`)**: Represents a single Point of Interest.
    *   **Attributes**:
        *   `id` (str): A unique, internally generated identifier.
        *   `name` (str): The human-readable name of the POI.
        *   `poi_type` (str): The category of the POI (e.g., "museum", "restaurant").
        *   `x`, `y` (Union[int, float]): Coordinates on the 1000x1000 grid.
        *   `attributes` (dict): A dictionary for custom key-value data.
    *   **Behavior**: Core properties (`id`, `name`, `x`, `y`) are immutable to ensure data integrity after creation. The `poi_type` and `attributes` are mutable to allow for dynamic management.

2.  **`Visitor` Class (`visitor.py`)**: Represents a user who visits POIs.
    *   **Attributes**:
        *   `id` (str): A unique, internally generated identifier.
        *   `name` (str): The visitor's name.
        *   `nationality` (str): The visitor's nationality.
        *   `visits` (list): A list of dictionaries, where each entry records a visit to a POI, including the `poi_id`, `date` (dd/mm/yyyy), and an optional `rating` (1-10).
    *   **Behavior**: Core properties (`id`, `name`, `nationality`) are immutable. The `visits` list is mutable, allowing for new visits to be recorded over time. Robust validation is built-in for date formats and rating ranges.

3.  **`PoiManagementSystem` Class (`main.py`)**: The central orchestrator that manages all POIs, Visitors, and their interactions.
    *   **State**: It holds lists of all `Poi` and `Visitor` objects, and a dictionary of all POI types and their known attributes.
    *   **Behavior**: It handles loading data from configuration, creating/deleting entities, enforcing system-wide rules (invariants), and executing all geospatial and analytical queries.

### Invariants (System Rules)

The system is designed to strictly enforce the following rules to maintain data consistency:

1.  **ID Uniqueness & Non-Reuse**: POI and Visitor IDs are generated internally using a timestamp-based method (`get_unique_id`) to ensure they are unique. Once an entity is deleted, its ID is never reused. This prevents historical data ambiguity.
2.  **Immutable Core Properties**: A POI's name and location, and a Visitor's name and nationality, cannot be changed after creation. This ensures that identifiers and core facts remain stable.
3.  **Referential Integrity on Deletion**:
    *   When a POI is deleted, all visit records associated with that POI are removed from every visitor's history.
    *   A POI type can only be deleted if no POIs are currently assigned to that type.
4.  **Coordinate Bounds**: All POIs must have coordinates `x` and `y` within the range `[0, 1000]`. The system validates this upon POI creation.

### Persistence Format

The system uses **YAML** for its initial configuration file. This format was chosen for its human-readability and its native support for nested structures (dictionaries and lists), which maps perfectly to the system's data model (POI types, POIs with attributes, visitors with visits). The system is designed to be robust, gracefully handling missing or extra fields during the loading process.

## 2. Edge Policies

To ensure deterministic and correct behavior, especially in ambiguous situations, the following policies have been implemented.

1.  **Boundary Correctness (ε)**: For queries listing POIs *exactly* at a certain distance (`get_pois_in_boundary`), a robust floating-point comparison is required. An epsilon-based check is used: `abs(distance - radius) <= epsilon`. The system's default epsilon is **`1e-9`**, which provides a good balance between precision and avoiding floating-point errors.

2.  **Tie-Break Rules**: For any query that returns a sorted list based on a count (e.g., "k most popular POIs," "k closest POIs"), ties are broken deterministically to ensure consistent results. The sorting order is:
    1.  Primary Key: The main metric (distance, visit count) in the specified order (ascending/descending).
    2.  Secondary Key: Entity ID (ascending).

3.  **Counting Rules**: The assignment specifies two types of counting, which the system adheres to:
    *   **Distinct by Default**: Queries like "number of visitors per POI" count each unique visitor only once, regardless of how many times they visited that POI.
    *   **Visit Event vs. Coverage**: Queries that explicitly ask for activity, such as "most active visitors," count the *total number of visits* (multiplicity matters).

4.  **Coordinate Bounds**: The map is a fixed 1000x1000 grid. Coordinates are validated to be within `0 <= x <= 1000` and `0 <= y <= 1000`. The system supports floating-point coordinates to allow for precise locations.

## 3. Usage Guide

This section provides a sample configuration and a simulated CLI session to demonstrate system usage.

### Sample Configuration (`configs/sample.yaml`)

```yaml
poi_types:
  museum:
    attributes: ["opening_hours", "entrance_fee", "exhibits"]
  restaurant:
    attributes: ["cuisine_type", "price_range", "seating_capacity"]
  park:
    attributes: ["area_size", "facilities", "pet_friendly"]

pois:
  - name: "Louvre Abu Dhabi"
    type: "museum"
    x: 500
    y: 300
    attributes:
      opening_hours: "10:00-18:00"
      entrance_fee: "63 AED"
      exhibits: "Art and Culture"
  - name: "Central Park"
    type: "park"
    x: 200
    y: 400
    attributes:
      area_size: "50 hectares"
      facilities: "playground, lake"
      pet_friendly: true

visitors:
  - name: "Ahmed Ali"
    nationality: "UAE"
    visits:
      - poi_name: "Louvre Abu Dhabi"
        date: "15/09/2024"
        rating: 9
```

### Install (only once)

```bash
# Clones the repository, goes to the directory and install the program
git clone https://github.com/murodbecks/yapoims.git
cd yapoims/
pip install -e .
```

### Sample Menu Session

```bash
# Start the system with the demo configuration
yapoims --demo
```

```text
============================================================
    YAPOIMS - Yet Another POI Management System
============================================================
Loaded: 3 POI types, 2 POIs, 1 visitors

========================================
MAIN MENU
========================================
1. POI Management
2. Visitor Management
3. POI Queries
4. Visitor & POI Analytics
5. System Information
6. Load/Save Configuration
0. Exit

Enter your choice: 1

------------------------------
POI MANAGEMENT
------------------------------
1. Add POI Type
2. Add POI
...
0. Back to Main Menu

Enter your choice: 2
Available POI types: museum, restaurant, park
Enter POI name: MBZUAI Campus
Enter POI type (or 'new' to create new type): new
Enter new POI type name: university
Creating new POI type 'university'...
Enter X coordinate (0-1000): 850
Enter Y coordinate (0-1000): 150

Enter values for university attributes (press Enter to skip):
POI 'MBZUAI Campus' added successfully.

Enter your choice: 0

========================================
MAIN MENU
========================================
...
Enter your choice: 2

------------------------------
VISITOR MANAGEMENT
------------------------------
1. Add Visitor
...
0. Back to Main Menu

Enter your choice: 1
Enter visitor name: Fatima Al-Mansoori
Enter visitor nationality: Emirati
Visitor 'Fatima Al-Mansoori' added successfully.

Enter your choice: 2
Available visitors:
1. Ahmed Ali (UAE)
2. Fatima Al-Mansoori (Emirati)
Select visitor: 2

Available POIs:
1. Louvre Abu Dhabi (museum)
2. Central Park (park)
3. MBZUAI Campus (university)
Select POI: 3
Enter visit date (dd/mm/yyyy): 01/10/2025
Enter rating (1-10, or press Enter to skip): 10
Visit added successfully: Fatima Al-Mansoori visited MBZUAI Campus

Enter your choice: 0

========================================
MAIN MENU
========================================
...
Enter your choice: 4

------------------------------
VISITOR & POI ANALYTICS
------------------------------
...
6. Coverage Fairness Analysis
0. Back to Main Menu

Enter your choice: 6
Enter minimum number of POIs visited (m): 2
Enter minimum number of distinct POI types (t): 2

Visitors with ≥2 POI visits across ≥2 distinct types:
Name                 Nationality     Total POIs    Distinct Types
----------------------------------------------------------------------
Ahmed Ali            UAE             2             2

Enter your choice: 0

========================================
MAIN MENU
========================================
...
Enter your choice: 0
Goodbye!
```