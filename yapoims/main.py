import os
import yaml
from typing import Union

from yapoims import Poi, Visitor
from yapoims.utils import get_unique_id, get_distance, check_type

class PoiManagementSystem:
    EPSILON = 1e-9

    def __init__(self, config_file_path: str = None):
        self._all_pois = []
        self._all_poi_types = {}
        self._all_visitors = []

        if config_file_path:
            self._load_config(config_file_path)
    
     # Getter methods
    def get_poi_types(self) -> dict:
        return self._all_poi_types.copy()

    def get_pois(self) -> list:
        return self._all_pois.copy()
    
    def get_visitors(self) -> list:
        return self._all_visitors.copy()

    # Loaders
    def _load_config(self, config_file_path: str) -> None:
        if not os.path.exists(config_file_path):
            print(f"Warning: '{config_file_path}' file does not exist. Initializing from scratch.")
            return 
        
        try:
            with open(config_file_path, 'r') as config_file:
                config = yaml.safe_load(config_file)
            
            if not config:
                print("Warning: Config file is empty or invalid")
                return
            
            if 'poi_types' in config:
                self._load_poi_types(config['poi_types'])
            
            if 'pois' in config:
                self._load_pois(config['pois'])
            
            if 'visitors' in config:
                self._load_visitors(config['visitors'])
        
        except Exception as e:
            print(f"Error loading config file: {e}")

    def _load_poi_types(self, poi_types: dict) -> None:
        check_type(poi_types, dict, "poi_types")
        
        for poi_type, attributes in poi_types.items():
            if (not isinstance(poi_type, str)) or (not isinstance(attributes, dict)):
                print(f"Warning: Invalid poi_type: {poi_type}. Skipping")
                continue
             
            poi_attributes = attributes.get('attributes')
            
            self.add_poi_type(poi_type, poi_attributes)

    def _load_pois(self, pois: list) -> None:
        check_type(pois, list, "pois")
        
        for poi in pois:
            if not isinstance(poi, dict):
                print(f"Warning: Invalid POI: {poi}")
                continue

            if not all([key_name in poi.keys() for key_name in ['name', 'type', 'x', 'y']]):
                print(f"Warning: Missing POI variables: {poi}")
                continue

            poi_name = poi['name']
            poi_type = poi['type']
            poi_x = poi['x']
            poi_y = poi['y']
            poi_attributes = poi.get('attributes', None)

            self.add_poi(poi_name, poi_type, poi_x, poi_y, poi_attributes)

    def _load_visitors(self, visitors: list) -> None:
        check_type(visitors, list, "visitors")
        
        for visitor in visitors:
            if not all([key_name in visitor.keys() for key_name in ['name', 'nationality']]):
                print(f"Warning: Missing Visitor variables: {visitor}")
                continue

            visitor_name = visitor['name']
            visitor_nationality = visitor['nationality']
            visitor_visits = visitor.get('visits', None)

            self.add_visitor(visitor_name, visitor_nationality, visitor_visits)

    # Adders
    def add_poi_type(self, poi_type: str, poi_attributes: list) -> bool:
        check_type(poi_type, str, "poi_type")
             
        if not isinstance(poi_attributes, list):
            poi_attributes = []

        poi_attributes = [poi_attribute for poi_attribute in poi_attributes if isinstance(poi_attribute, str)]
        self._all_poi_types[poi_type] = {"attributes": poi_attributes, "num_pois": 0}

        return True

    def add_poi(self, poi_name: str, poi_type: str, poi_x: Union[int, float], poi_y: Union[int, float], poi_attributes: dict = None) -> bool:
        check_type(poi_name, str, "poi_name")
        check_type(poi_type, str, "poi_type")
        check_type(poi_x, Union[int, float], "poi_x")
        check_type(poi_y, Union[int, float], "poi_y")

        if poi_x < 0 or poi_x > 1000:
            print(f"Warning: Invalid value for POI `x`: {poi_x}")
            return False
        
        if poi_y < 0 or poi_y > 1000:
            print(f"Warning: Invalid value for POI `y`: {poi_y}")
            return False

        if not isinstance(poi_attributes, dict):
            poi_attributes = None
        
        poi_id = get_unique_id('poi_')
        poi_instance = Poi(poi_id, poi_name, poi_type, poi_x, poi_y, poi_attributes)
        self._all_pois.append(poi_instance)
        self._add_poi_to_poi_types(poi_instance)

        return True
    
    def _add_poi_to_poi_types(self, poi) -> None:
        poi_type = poi.get_poi_type()
        
        if poi_type not in self.get_poi_types().keys():
            self._all_poi_types[poi_type] = {"attributes": poi.get_attribute_names(), "num_pois": 0}
        else:
            missing_attributes = [attribute for attribute in poi.get_attribute_names() if attribute not in self._all_poi_types[poi_type]['attributes']]
            self._all_poi_types[poi_type]['attributes'].extend(missing_attributes)
        
        self._all_poi_types[poi_type]['num_pois'] += 1

    def add_visitor(self, visitor_name: str, visitor_nationality: str, visitor_visits: list) -> bool:
        check_type(visitor_name, str, "visitor_name")
        check_type(visitor_nationality, str, "visitor_nationality")

        if not isinstance(visitor_visits, list):
            visitor_visits = []
        
        visitor_visits_updated = []
        for visit in visitor_visits:
            poi_name = visit['poi_name']
            
            poi_id = None
            for poi in self.get_pois():
                if poi.get_name() == poi_name:
                    poi_id = poi.get_id()
            
            if poi_id is not None:
                visitor_visits_updated.append({"poi_id": poi_id, "date": visit.get("date"), "rating": visit.get("rating")})
        
        visitor_id = get_unique_id('u_')
        self._all_visitors.append(Visitor(visitor_id, visitor_name, visitor_nationality, visitor_visits_updated))

        return True
    
    def add_poi_type_attribute(self, poi_type: str, attribute: str) -> bool:
        check_type(poi_type, str, "poi_type")
        check_type(attribute, str, "attribute")
        
        if poi_type not in self.get_poi_types():
            self.add_poi_type(poi_type, [attribute])
        else:
            self._all_poi_types[poi_type]['attributes'].append(attribute)
        
        return True

    
    # Deleters
    def delete_poi_type(self, poi_type: str) -> bool:
        check_type(poi_type, str, "poi_type")
        
        if poi_type not in self.get_poi_types().keys():
            print(f"Warning: No {poi_type} exist in POI types")
            return False
        
        elif self._all_poi_types[poi_type]['num_pois'] != 0:
            print(f"Warning: {poi_type} has more than 0 POIs. Not deleting.")
            return False
        
        else:
            del self._all_poi_types[poi_type]
            return True

    def delete_poi(self, poi_name: str) -> bool:
        check_type(poi_name, str, "poi_name")
        
        poi_idx_to_delete = None
        for i, poi in enumerate(self.get_pois()):
            if poi.get_name() == poi_name:
                poi_idx_to_delete = i
                break
        
        if poi_idx_to_delete is None:
            print(f"Warning: Trying to delete non-existent POI: {poi_name}")
            return False

        poi_to_delete = self._all_pois.pop(poi_idx_to_delete)
        poi_id_to_delete = poi_to_delete.get_id()
        poi_type = poi_to_delete.get_poi_type()

        if poi_type in self._all_poi_types:
            self._all_poi_types[poi_type]['num_pois'] -= 1

        for visitor in self._all_visitors:
            all_visits = visitor.get_visits()
            for visit in all_visits:
                if visit['poi_id'] == poi_id_to_delete:
                    visitor.delete_visit(poi_id_to_delete)
        
        return True

    def delete_visitor(self, visitor_name: str) -> bool:
        check_type(visitor_name, str, "visitor_name")

        visitor_idx_to_delete = None
        for i, visitor in enumerate(self.get_visitors()):
            if visitor.get_name() == visitor_name:
                visitor_idx_to_delete = i
                break
        
        if visitor_idx_to_delete is None:
            print(f"Warning: Trying to delete non-existent Visitor: {visitor_name}")
            return False

        visitor_to_delete = self._all_visitors.pop(visitor_idx_to_delete)
        return True


    def delete_poi_type_attribute(self, poi_type: str, attribute: str) -> bool:
        check_type(poi_type, str, "poi_type")
        check_type(attribute, str, "attribute")
        
        if poi_type in self.get_poi_types():
            if attribute in self._all_poi_types[poi_type]['attributes']:
                self._all_poi_types[poi_type]['attributes'].remove(attribute)
        
        return True
    
    # Renamers
    def rename_poi_type(self, old_poi_type: str, new_poi_type: str) -> bool:
        check_type(old_poi_type, str, "old_poi_type")
        check_type(new_poi_type, str, "new_poi_type")
        
        if old_poi_type not in self.get_poi_types():
            print(f"Warning: `{old_poi_type}` is non-existent in POI types")
            return False
        
        self._all_poi_types[new_poi_type] = self._all_poi_types.pop(old_poi_type)

        for poi in self._all_pois:
            if poi.get_poi_type() == old_poi_type:
                poi.set_poi_type(new_poi_type)
        
        return True

    def rename_poi_type_attribute(self, poi_type: str, old_poi_attribute: str, new_poi_attribute: str) -> bool:
        check_type(poi_type, str, "poi_type")
        check_type(old_poi_attribute, str, "old_poi_attribute")
        check_type(new_poi_attribute, str, "new_poi_attribute")
        
        if poi_type not in self.get_poi_types():
            print(f"Warning: `{poi_type}` is non-existent in POI types.")
            return False
        
        if old_poi_attribute not in self._all_poi_types[poi_type]['attributes']:
            print(f"Warning: `{old_poi_attribute}` is non-existent in {poi_type} attributes.")
            return False
        
        current_attributes = self._all_poi_types[poi_type]['attributes']
        new_attributes = [new_poi_attribute if attribute == old_poi_attribute else attribute for attribute in current_attributes]
        self._all_poi_types[poi_type]['attributes'] = new_attributes

        for poi in self._all_pois:
            if old_poi_attribute in poi.get_attributes():
                poi.change_attribute_name(old_poi_attribute, new_poi_attribute)
        
        return True
    
    # Queries for POIs
    def get_pois_by_poi_type(self, poi_type: str) -> list:
        check_type(poi_type, str, "poi_type")

        selected_pois = []
        for poi in self.get_pois():
            if poi.get_poi_type() == poi_type:
                selected_pois.append(poi)
        
        return selected_pois

    def get_nearest_pois(self) -> list:
        # getting the largest distance as a starting
        smallest_distance = get_distance(0, 0, 1000, 1000)

        num_pois = len(self.get_pois())
        selected_pois = []
        for i in range(num_pois):
            for j in range(i+1, num_pois):
                poi1 = self.get_pois()[i]
                poi2 = self.get_pois()[j]

                x1, y1 = poi1.get_coordinates()
                x2, y2 = poi2.get_coordinates()

                distance = get_distance(x1, y1, x2, y2)

                if distance < smallest_distance:
                    smallest_distance = distance
                    selected_pois = [(poi1.get_id(), poi1.get_name(), poi1.get_coordinates()), 
                                     (poi2.get_id(), poi2.get_name(), poi2.get_coordinates())]

        return selected_pois

        
    def get_num_pois_per_poi_type(self):
        poi_info = {}

        for poi_type, attributes in self.get_poi_types().items():
            poi_info[poi_type] = attributes['num_pois']
        
        return poi_info

    def get_pois_within_distance(self, x: Union[int, float], y: Union[int, float], 
                                 r: Union[int, float], epsilon: float = None) -> list:
        check_type(x, Union[int, float], "x")
        check_type(y, Union[int, float], "y")
        check_type(r, Union[int, float], "r")

        if epsilon is None:
            epsilon = self.EPSILON

        if not (0 <= x <= 1000) or not (0 <= y <= 1000):
            print(f"Warning: Coordinates ({x}, {y}) outside map bounds (0-1000)")
            return []
        
        if r < 0:
            print("Warning: Radius cannot be negative")
            return []

        selected_pois = []
        for poi in self.get_pois():
            poi_x, poi_y = poi.get_coordinates()
            distance = get_distance(x, y, poi_x, poi_y)

            if distance <= r + epsilon:
                selected_pois.append((poi.get_id(), poi.get_name(), (poi_x, poi_y), 
                                      poi.get_poi_type(), distance))
        
        return selected_pois

    def get_k_closest_pois(self, x: Union[int, float], y: Union[int, float], k: int) -> list:
        check_type(x, Union[int, float], "x")
        check_type(y, Union[int, float], "y")
        check_type(k, int, "k")

        num_pois = len(self.get_pois())
        if k > num_pois:
            print(f"Requested more than number of POIs in the system. Returning all ({num_pois}) POIs.")
            k = num_pois
        
        selected_pois = []
        for poi in self.get_pois():
            poi_x, poi_y = poi.get_coordinates()
            distance = get_distance(x, y, poi_x, poi_y)
            selected_pois.append((poi.get_id(), poi.get_name(), (poi_x, poi_y), 
                                    poi.get_poi_type(), distance))
        
        # Sort by distance (ascending), then by id (ascending), then by name (ascending)
        sorted_pois = sorted(selected_pois, key=lambda poi: (poi[4], poi[0], poi[1]))
        return sorted_pois[:k]

    def get_pois_in_boundary(self, x: Union[int, float], y: Union[int, float], r: Union[int, float], epsilon: float = None) -> list:
        check_type(x, Union[int, float], "x")
        check_type(y, Union[int, float], "y")
        check_type(r, Union[int, float], "r")

        if epsilon is None:
            epsilon = self.EPSILON

        if not (0 <= x <= 1000) or not (0 <= y <= 1000):
            print(f"Warning: Coordinates ({x}, {y}) outside map bounds (0-1000)")
            return []
        
        if r < 0:
            print("Warning: Radius cannot be negative")
            return []
        
        if epsilon <= 0:
            print(f"Warning: Epsilon must be positive, got {epsilon}")
            return []

        selected_pois = []
        for poi in self.get_pois():
            poi_x, poi_y = poi.get_coordinates()
            distance = get_distance(x, y, poi_x, poi_y)

            if abs(distance - r) <= epsilon:
                selected_pois.append((poi.get_id(), poi.get_name(), (poi_x, poi_y), 
                                      poi.get_poi_type(), distance))
        
        return selected_pois

    # Queries for Visitors and POIs
    def get_visited_pois(self, visitor_name: str) -> tuple:
        check_type(visitor_name, str, "visitor_name")

        for visitor in self.get_visitors():
            if visitor.get_name() == visitor_name:
                selected_pois = []
                for visit in visitor.get_visits():
                    for poi in self.get_pois():
                        if poi.get_id() == visit['poi_id']:
                            selected_pois.append((visit['poi_id'], poi.get_name(), visit['date']))

                return selected_pois
        
        print(f"`{visitor_name}` not in Visitors")
        return []

    def get_num_visitors_per_poi(self) -> list:
        poi_info = []

        for poi in self.get_pois():
            poi_id = poi.get_id()
            num_visitors = 0

            for visitor in self.get_visitors():
                num_visitors += len(visitor.get_visits_to_poi(poi_id))
            
            poi_info.append((poi_id, num_visitors))
        
        return poi_info

    def get_num_pois_per_visitor(self) -> list:
        visitor_info = []
        for visitor in self.get_visitors():
            visitor_info.append((visitor.get_id(), visitor.get_num_visits()))
        
        return visitor_info

    def get_crowdest_k_pois(self, k: int) -> list:
        check_type(k, int, "k")

        num_pois = len(self.get_pois())
        if k > num_pois:
            print(f"Requested more than number of POIs in the system. Returning all ({num_pois}) POIs.")
            k = num_pois
        
        num_visitors_per_poi = self.get_num_visitors_per_poi()
        sorted_num_visitors_per_poi = sorted(num_visitors_per_poi, key=lambda visit: (-visit[1], visit[0]))

        num_visitors_per_poi_info = []
        for visit in sorted_num_visitors_per_poi:
            poi_id, _ = visit
            for poi in self.get_pois():
                if poi.get_id() == poi_id:
                    num_visitors_per_poi_info.append((poi_id, poi.get_name()))
        
        return num_visitors_per_poi_info[:k]

    def get_most_visited_k_visitors(self, k: int) -> list:
        check_type(k, int, "k")

        num_visitors = len(self.get_visitors())
        if k > num_visitors:
            print(f"Requested more than number of POIs in the system. Returning all ({num_visitors}) Visitors.")
            k = num_visitors

        num_pois_per_visitor = self.get_num_pois_per_visitor()
        sorted_num_visitors_per_poi = sorted(num_pois_per_visitor, key=lambda visit: (-visit[1], visit[0]))
        
        num_visitors_per_poi_info = []
        for visit in sorted_num_visitors_per_poi:
            visitor_id, _ = visit
            for visitor in self.get_visitors():
                if visitor.get_id() == visitor_id:
                    num_visitors_per_poi_info.append((visitor_id, visitor.get_name()))
        
        return num_visitors_per_poi_info[:k]

    def get_special_visitors(self, m: int, t: int) -> list:
        # (visitor id, name, nationality, total number of POIs visited, number of distinct POI types)
        check_type(m, int, "m")
        check_type(t, int, "t")

        selected_visitors = []
        for visitor in self.get_visitors():
            num_visits = visitor.get_num_visits()

            if num_visits < m:
                continue

            visited_poi_ids = set(visitor.get_visited_poi_ids())
            visited_poi_types = set()

            for poi in self.get_pois():
                if poi.get_id() in visited_poi_ids:
                    visited_poi_types.add(poi.get_poi_type())
            
            if len(visited_poi_types) < t:
                continue

            selected_visitors.append((visitor.get_id(), visitor.get_name(), visitor.get_nationality(), num_visits, len(visited_poi_types)))

        return selected_visitors

    # dunder functions
    def __repr__(self) -> str:
        return f"PoiManagementSystem(poi_types={self.get_poi_types()}, pois={self.get_pois()}, visitors={self.get_visitors()})"
    
    def __eq__(self, other_poims) -> bool:
        if not isinstance(other_poims, PoiManagementSystem):
            return False
        
        return (self.get_poi_types(), self.get_pois(), self.get_visitors()) == \
               (other_poims.get_poi_types(), other_poims.get_pois(), other_poims.get_visitors())

if __name__ == "__main__":
    print("=== YAPOIMS - Yet Another POI Management System ===")
    print("Demo: Loading configuration and testing core functionality\n")
    
    # 1. Initialize system with config file
    print("1. Loading system from config file...")
    poims = PoiManagementSystem('configs/sample.yaml')
    
    print(f"   ✓ Loaded {len(poims.get_poi_types())} POI types")
    print(f"   ✓ Loaded {len(poims.get_pois())} POIs")
    print(f"   ✓ Loaded {len(poims.get_visitors())} visitors")
    print()
    
    # 2. Display loaded data
    print("2. System Overview:")
    print("   POI Types:", list(poims.get_poi_types().keys()))
    for poi in poims.get_pois():
        print(f"   POI: {poi.get_name()} ({poi.get_poi_type()}) at {poi.get_coordinates()}")
    for visitor in poims.get_visitors():
        print(f"   Visitor: {visitor.get_name()} ({visitor.get_nationality()}) - {visitor.get_num_visits()} visits")
    print()
    
    # 3. Adding new data dynamically
    print("3. Adding new POI and visitor...")
    success = poims.add_poi("Marina Beach", "beach", 750, 200, {
        "length_km": "13", 
        "facilities": "restaurants, parking",
        "swimming_allowed": False
    })
    print(f"   Added Marina Beach: {'✓' if success else '✗'}")
    
    success = poims.add_visitor("Sara Ahmed", "Egyptian", [
        {"poi_name": "Louvre Abu Dhabi", "date": "10/10/2024", "rating": 9},
        {"poi_name": "Marina Beach", "date": "11/10/2024", "rating": 8}
    ])
    print(f"   Added Sara Ahmed: {'✓' if success else '✗'}")
    print()
    
    # 4. POI Queries
    print("4. POI Queries:")
    
    # 4.1 POIs by type
    museums = poims.get_pois_by_poi_type("museum")
    print(f"   Museums: {[poi.get_name() for poi in museums]}")
    
    # 4.2 Nearest POI pair
    nearest_pair = poims.get_nearest_pois()
    if nearest_pair:
        print(f"   Closest POI pair: {nearest_pair[0][1]} & {nearest_pair[1][1]}")
    
    # 4.3 POIs within radius
    center_x, center_y, radius = 500, 400, 300
    nearby_pois = poims.get_pois_within_distance(center_x, center_y, radius)
    print(f"   POIs within {radius}m of ({center_x},{center_y}):")
    for poi_id, name, coords, poi_type, dist in nearby_pois:
        print(f"     - {name}: {dist:.1f}m away")
    
    # 4.4 K closest POIs
    k_closest = poims.get_k_closest_pois(400, 300, k=2)
    print(f"   2 closest POIs to (400,300):")
    for poi_id, name, coords, poi_type, dist in k_closest:
        print(f"     - {name}: {dist:.1f}m away")
    print()
    
    # 5. Visitor & POI Relationship Queries
    print("5. Visitor & POI Analytics:")
    
    # 5.1 Visitor's POI history
    sara_visits = poims.get_visited_pois("Sara Ahmed")
    print(f"   Sara Ahmed's visits: {len(sara_visits)} POIs")
    for poi_id, name, date in sara_visits:
        print(f"     - {name} on {date}")
    
    # 5.2 POI popularity
    poi_popularity = poims.get_num_visitors_per_poi()
    print("   POI Popularity (visitors count):")
    for poi_id, count in poi_popularity:
        poi_name = next(poi.get_name() for poi in poims.get_pois() if poi.get_id() == poi_id)
        print(f"     - {poi_name}: {count} visitors")
    
    # 5.3 Most active visitors
    active_visitors = poims.get_most_visited_k_visitors(k=2)
    print(f"   Most active visitors:")
    for visitor_id, name in active_visitors:
        visits_count = next(v.get_num_visits() for v in poims.get_visitors() if v.get_id() == visitor_id)
        print(f"     - {name}: {visits_count} visits")
    
    # 5.4 Coverage fairness analysis
    special_visitors = poims.get_special_visitors(m=2, t=2)
    print(f"   Visitors with ≥2 visits across ≥2 POI types:")
    for v_id, name, nationality, total_pois, distinct_types in special_visitors:
        print(f"     - {name} ({nationality}): {total_pois} visits, {distinct_types} types")
    print()
    
    # 6. Dynamic Management Operations
    print("6. Dynamic Management:")
    
    # 6.1 Add new POI type with attribute
    poims.add_poi_type("shopping_mall", ["stores_count", "parking_spaces", "food_court"])
    print("   ✓ Added 'shopping_mall' POI type")
    
    # 6.2 Add POI of new type
    poims.add_poi("City Mall", "shopping_mall", 300, 600, {
        "stores_count": "150",
        "parking_spaces": "500",
        "food_court": True
    })
    print("   ✓ Added City Mall")
    
    # 6.3 Rename POI type attribute
    success = poims.rename_poi_type_attribute("shopping_mall", "stores_count", "number_of_stores")
    print(f"   Renamed attribute: {'✓' if success else '✗'}")
    print()
    
    # 7. Boundary Correctness Demo (Epsilon-based)
    print("7. Boundary Correctness (Epsilon-based):")
    
    # Add a POI at exact mathematical distance
    poims.add_poi("Boundary Test", "test", 103, 104, {})  # Distance = 5.0 from (100,100)
    
    # Test exact boundary detection
    exact_boundary = poims.get_pois_in_boundary(100, 100, 5.0, epsilon=1e-9)
    print(f"   POIs exactly at distance 5.0: {len(exact_boundary)}")
    
    # Test with smaller epsilon
    strict_boundary = poims.get_pois_in_boundary(100, 100, 5.0, epsilon=1e-15)
    print(f"   POIs with strict epsilon: {len(strict_boundary)}")
    print()
    
    # 8. System Statistics Summary
    print("8. Final System Statistics:")
    poi_counts = poims.get_num_pois_per_poi_type()
    print("   POI Type Distribution:")
    for poi_type, count in poi_counts.items():
        print(f"     - {poi_type}: {count} POIs")
    
    print(f"   Total POIs: {len(poims.get_pois())}")
    print(f"   Total Visitors: {len(poims.get_visitors())}")
    print(f"   Total POI Types: {len(poims.get_poi_types())}")
    
    print("\n=== Demo completed successfully! ===")
    
    # 9. Optional: Error handling demonstration
    print("\n9. Error Handling Examples:")
    
    # Try invalid coordinate
    invalid_pois = poims.get_pois_within_distance(-10, 2000, 100)
    print(f"   Invalid coordinates result: {len(invalid_pois)} POIs")
    
    # Try to delete non-existent POI
    delete_success = poims.delete_poi("Non-existent POI")
    print(f"   Delete non-existent POI: {'✓' if delete_success else '✗'}")
    
    # Try to delete POI type with existing POIs
    delete_type_success = poims.delete_poi_type("museum")  # Has POIs
    print(f"   Delete POI type with POIs: {'✓' if delete_type_success else '✗'}")