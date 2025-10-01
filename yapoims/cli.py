import sys
import argparse
from typing import Optional
from yapoims.main import PoiManagementSystem

class PoiManagementCLI:
    def __init__(self, config_file: Optional[str] = None):
        self.system = PoiManagementSystem(config_file)
        self.running = True
    
    def run(self):
        """Main CLI loop"""
        self.display_welcome()
        
        while self.running:
            self.display_main_menu()
            choice = input("\nEnter your choice: ").strip()
            self.handle_main_menu(choice)
    
    def display_welcome(self):
        print("=" * 60)
        print("    YAPOIMS - Yet Another POI Management System")
        print("=" * 60)
        if len(self.system.get_pois()) > 0:
            print(f"Loaded: {len(self.system.get_poi_types())} POI types, "
                  f"{len(self.system.get_pois())} POIs, "
                  f"{len(self.system.get_visitors())} visitors")
        print()
    
    def display_main_menu(self):
        print("\n" + "=" * 40)
        print("MAIN MENU")
        print("=" * 40)
        print("1. POI Management")
        print("2. Visitor Management") 
        print("3. POI Queries")
        print("4. Visitor & POI Analytics")
        print("5. System Information")
        print("6. Load/Save Configuration")
        print("0. Exit")

    def display_poi_management_menu(self):
        print("\n" + "-" * 30)
        print("POI MANAGEMENT")
        print("-" * 30)
        print("1. Add POI Type")
        print("2. Add POI")
        print("3. Delete POI")
        print("4. Delete POI Type")
        print("5. List POIs by Type")
        print("6. Rename POI Type")
        print("7. Manage POI Type Attributes")
        print("8. View All POI Types")
        print("9. View All POIs")
        print("0. Back to Main Menu")

    def display_visitor_management_menu(self):
        print("\n" + "-" * 30)
        print("VISITOR MANAGEMENT")
        print("-" * 30)
        print("1. Add Visitor")
        print("2. Add Visit to POI")
        print("3. List All Visitors")
        print("4. View Visitor Details")
        print("5. View All Visitors (Detailed)")
        print("0. Back to Main Menu")

    def display_poi_queries_menu(self):
        print("\n" + "-" * 30)
        print("POI QUERIES")
        print("-" * 30)
        print("1. List POIs by Type")
        print("2. Find Nearest POI Pair")
        print("3. Count POIs per Type")
        print("4. POIs Within Radius")
        print("5. K Closest POIs")
        print("6. POIs at Exact Distance (Boundary)")
        print("0. Back to Main Menu")

    def display_visitor_analytics_menu(self):
        print("\n" + "-" * 30)
        print("VISITOR & POI ANALYTICS")
        print("-" * 30)
        print("1. Visitor's POI History")
        print("2. Visitors per POI")
        print("3. POIs per Visitor")
        print("4. Most Active Visitors")
        print("5. Most Popular POIs")
        print("6. Coverage Fairness Analysis")
        print("0. Back to Main Menu")

    def display_system_info_menu(self):
        print("\n" + "-" * 30)
        print("SYSTEM INFORMATION")
        print("-" * 30)
        print("1. Overall Statistics")
        print("2. POI Type Details")
        print("3. Map Boundary Info")
        print("4. Quick System Overview")
        print("0. Back to Main Menu")

    def display_config_menu(self):
        print("\n" + "-" * 30)
        print("CONFIGURATION MANAGEMENT")
        print("-" * 30)
        print("1. Load Configuration File")
        print("2. Save Current State (Demo)")
        print("3. System Validation Report")
        print("0. Back to Main Menu")

    def get_valid_int(self, prompt: str, min_val: int = None, max_val: int = None) -> int:
        while True:
            try:
                value = int(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Value must be >= {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    print(f"Value must be <= {max_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid integer.")

    def get_valid_float(self, prompt: str, min_val: float = None) -> float:
        while True:
            try:
                value = float(input(prompt))
                if min_val is not None and value < min_val:
                    print(f"Value must be >= {min_val}")
                    continue
                return value
            except ValueError:
                print("Please enter a valid number.")

    # === MAIN MENU HANDLERS ===
    def handle_main_menu(self, choice: str):
        if choice == "1":
            self.poi_management_submenu()
        elif choice == "2":
            self.visitor_management_submenu()
        elif choice == "3":
            self.poi_queries_submenu()
        elif choice == "4":
            self.visitor_analytics_submenu()
        elif choice == "5":
            self.system_information_submenu()
        elif choice == "6":
            self.config_management_submenu()
        elif choice == "0":
            print("Goodbye!")
            self.running = False
        else:
            print("Invalid choice. Please try again.")

    # === POI MANAGEMENT ===
    def poi_management_submenu(self):
        while True:
            self.display_poi_management_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_poi_management_menu(choice)

    def handle_poi_management_menu(self, choice: str):
        if choice == "1":
            self.add_poi_type()
        elif choice == "2":
            self.add_poi()
        elif choice == "3":
            self.delete_poi()
        elif choice == "4":
            self.delete_poi_type()
        elif choice == "5":
            self.list_pois_by_type()
        elif choice == "6":
            self.rename_poi_type()
        elif choice == "7":
            self.manage_poi_type_attributes()
        elif choice == "8":
            self.view_all_poi_types()
        elif choice == "9":
            self.view_all_pois()
        else:
            print("Invalid choice. Please try again.")
    
    def add_poi_type(self):
        poi_type = input("Enter POI type name: ").strip()
        if not poi_type:
            print("POI type name cannot be empty.")
            return
        
        if poi_type in self.system.get_poi_types():
            print(f"POI type '{poi_type}' already exists.")
            return
        
        print("Enter attributes for this POI type (press Enter with empty line to finish):")
        attributes = []
        while True:
            attr = input(f"Attribute {len(attributes) + 1}: ").strip()
            if not attr:
                break
            attributes.append(attr)
        
        success = self.system.add_poi_type(poi_type, attributes)
        if success:
            print(f"POI type '{poi_type}' added successfully with {len(attributes)} attributes.")
        else:
            print("Failed to add POI type.")

    def add_poi(self):
        # Display available POI types
        poi_types = list(self.system.get_poi_types().keys())
        if not poi_types:
            print("No POI types available. Please add a POI type first.")
            return
        
        print("Available POI types:", ", ".join(poi_types))
        
        name = input("Enter POI name: ").strip()
        if not name:
            print("POI name cannot be empty.")
            return
            
        poi_type = input("Enter POI type (or 'new' to create new type): ").strip()
        
        # Allow creating new POI type on the fly
        if poi_type == "new" or poi_type not in poi_types:
            if poi_type != "new":
                create_new = input(f"POI type '{poi_type}' doesn't exist. Create it? (y/N): ").strip().lower()
                if create_new != 'y':
                    return
            else:
                poi_type = input("Enter new POI type name: ").strip()
                
            if poi_type and poi_type not in poi_types:
                print(f"Creating new POI type '{poi_type}'...")
                self.system.add_poi_type(poi_type, [])
                poi_types.append(poi_type)
        
        try:
            x = self.get_valid_float("Enter X coordinate (0-1000): ", 0)
            y = self.get_valid_float("Enter Y coordinate (0-1000): ", 0)
            
            if x > 1000 or y > 1000:
                print("Coordinates must be within 1000x1000 grid.")
                return
        except KeyboardInterrupt:
            return
        
        # Get attributes for this POI type
        type_attributes = self.system.get_poi_types()[poi_type]['attributes']
        attributes = {}
        
        if type_attributes:
            print(f"\nEnter values for {poi_type} attributes (press Enter to skip):")
            for attr in type_attributes:
                value = input(f"{attr}: ").strip()
                if value:
                    # Try to convert to appropriate type
                    if value.lower() in ['true', 'false']:
                        attributes[attr] = value.lower() == 'true'
                    elif value.isdigit():
                        attributes[attr] = int(value)
                    else:
                        try:
                            attributes[attr] = float(value)
                        except ValueError:
                            attributes[attr] = value
        
        success = self.system.add_poi(name, poi_type, x, y, attributes)
        if success:
            print(f"POI '{name}' added successfully.")
        else:
            print("Failed to add POI.")

    def delete_poi(self):
        pois = self.system.get_pois()
        if not pois:
            print("No POIs available to delete.")
            return
        
        print("\nAvailable POIs:")
        for i, poi in enumerate(pois, 1):
            print(f"{i}. {poi.get_name()} ({poi.get_poi_type()}) at {poi.get_coordinates()}")
        
        try:
            choice = self.get_valid_int("Enter POI number to delete: ", 1, len(pois))
            poi_to_delete = pois[choice - 1]
            
            confirm = input(f"Are you sure you want to delete '{poi_to_delete.get_name()}'? (y/N): ").strip().lower()
            if confirm == 'y':
                success = self.system.delete_poi(poi_to_delete.get_name())
                if success:
                    print(f"POI '{poi_to_delete.get_name()}' deleted successfully.")
                else:
                    print("Failed to delete POI.")
            else:
                print("Deletion cancelled.")
        except KeyboardInterrupt:
            return

    def delete_poi_type(self):
        poi_types = self.system.get_poi_types()
        if not poi_types:
            print("No POI types available to delete.")
            return
            
        print("Available POI types:")
        for poi_type, info in poi_types.items():
            print(f"  - {poi_type}: {info['num_pois']} POIs")
        
        poi_type = input("Enter POI type to delete: ").strip()
        if poi_type not in poi_types:
            print(f"POI type '{poi_type}' not found.")
            return
            
        if poi_types[poi_type]['num_pois'] > 0:
            print(f"Cannot delete POI type '{poi_type}': it has {poi_types[poi_type]['num_pois']} POIs.")
            return
            
        confirm = input(f"Are you sure you want to delete POI type '{poi_type}'? (y/N): ").strip().lower()
        if confirm == 'y':
            success = self.system.delete_poi_type(poi_type)
            if success:
                print(f"POI type '{poi_type}' deleted successfully.")
            else:
                print("Failed to delete POI type.")

    def list_pois_by_type(self):
        poi_type = input("Enter POI type: ").strip()
        pois = self.system.get_pois_by_poi_type(poi_type)
        self.display_pois_list(pois, f"POIs of type '{poi_type}'")

    def rename_poi_type(self):
        poi_types = list(self.system.get_poi_types().keys())
        if not poi_types:
            print("No POI types available.")
            return
            
        print("Available POI types:", ", ".join(poi_types))
        old_name = input("Enter current POI type name: ").strip()
        
        if old_name not in poi_types:
            print(f"POI type '{old_name}' not found.")
            return
            
        new_name = input("Enter new POI type name: ").strip()
        if not new_name:
            print("New name cannot be empty.")
            return
            
        if new_name in poi_types:
            print(f"POI type '{new_name}' already exists.")
            return
            
        success = self.system.rename_poi_type(old_name, new_name)
        if success:
            print(f"POI type renamed from '{old_name}' to '{new_name}' successfully.")
        else:
            print("Failed to rename POI type.")

    def manage_poi_type_attributes(self):
        poi_types = list(self.system.get_poi_types().keys())
        if not poi_types:
            print("No POI types available.")
            return
            
        print("Available POI types:", ", ".join(poi_types))
        poi_type = input("Enter POI type: ").strip()
        
        if poi_type not in poi_types:
            print(f"POI type '{poi_type}' not found.")
            return
            
        while True:
            attributes = self.system.get_poi_types()[poi_type]['attributes']
            print(f"\nCurrent attributes for '{poi_type}': {attributes}")
            print("\n1. Add attribute")
            print("2. Remove attribute")
            print("3. Rename attribute")
            print("0. Back")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                attr = input("Enter new attribute name: ").strip()
                if attr:
                    self.system.add_poi_type_attribute(poi_type, attr)
                    print(f"Attribute '{attr}' added.")
            elif choice == "2":
                if not attributes:
                    print("No attributes to remove.")
                    continue
                print("Current attributes:", ", ".join(attributes))
                attr = input("Enter attribute to remove: ").strip()
                if attr in attributes:
                    self.system.delete_poi_type_attribute(poi_type, attr)
                    print(f"Attribute '{attr}' removed.")
                else:
                    print(f"Attribute '{attr}' not found.")
            elif choice == "3":
                if not attributes:
                    print("No attributes to rename.")
                    continue
                print("Current attributes:", ", ".join(attributes))
                old_attr = input("Enter current attribute name: ").strip()
                if old_attr in attributes:
                    new_attr = input("Enter new attribute name: ").strip()
                    if new_attr:
                        success = self.system.rename_poi_type_attribute(poi_type, old_attr, new_attr)
                        if success:
                            print(f"Attribute renamed from '{old_attr}' to '{new_attr}'.")
                        else:
                            print("Failed to rename attribute.")
                else:
                    print(f"Attribute '{old_attr}' not found.")

    def display_pois_list(self, pois, title):
        print(f"\n{title}:")
        if not pois:
            print("No POIs found.")
            return
        
        print(f"{'Name':<25} {'Type':<15} {'Coordinates':<15} {'Attributes'}")
        print("-" * 80)
        for poi in pois:
            attrs_str = str(poi.get_attributes())[:30] + "..." if len(str(poi.get_attributes())) > 30 else str(poi.get_attributes())
            print(f"{poi.get_name():<25} {poi.get_poi_type():<15} {str(poi.get_coordinates()):<15} {attrs_str}")

    # === VISITOR MANAGEMENT ===
    def visitor_management_submenu(self):
        while True:
            self.display_visitor_management_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_visitor_management_menu(choice)

    def handle_visitor_management_menu(self, choice: str):
        if choice == "1":
            self.add_visitor()
        elif choice == "2":
            self.add_visit()
        elif choice == "3":
            self.list_all_visitors()
        elif choice == "4":
            self.view_visitor_details()
        elif choice == "5":
            self.view_all_visitors_detailed()
        else:
            print("Invalid choice. Please try again.")

    def add_visitor(self):
        name = input("Enter visitor name: ").strip()
        nationality = input("Enter visitor nationality: ").strip()
        
        if not name or not nationality:
            print("Name and nationality cannot be empty.")
            return
        
        success = self.system.add_visitor(name, nationality, [])
        if success:
            print(f"Visitor '{name}' added successfully.")
        else:
            print("Failed to add visitor.")

    def add_visit(self):
        visitors = self.system.get_visitors()
        pois = self.system.get_pois()
        
        if not visitors:
            print("No visitors available. Please add a visitor first.")
            return
            
        if not pois:
            print("No POIs available. Please add a POI first.")
            return
        
        print("Available visitors:")
        for i, visitor in enumerate(visitors, 1):
            print(f"{i}. {visitor.get_name()} ({visitor.get_nationality()})")
        
        try:
            visitor_choice = self.get_valid_int("Select visitor: ", 1, len(visitors))
            selected_visitor = visitors[visitor_choice - 1]
        except KeyboardInterrupt:
            return
        
        print("\nAvailable POIs:")
        for i, poi in enumerate(pois, 1):
            print(f"{i}. {poi.get_name()} ({poi.get_poi_type()})")
        
        try:
            poi_choice = self.get_valid_int("Select POI: ", 1, len(pois))
            selected_poi = pois[poi_choice - 1]
        except KeyboardInterrupt:
            return
        
        date = input("Enter visit date (dd/mm/yyyy): ").strip()
        rating_input = input("Enter rating (1-10, or press Enter to skip): ").strip()
        
        rating = None
        if rating_input:
            try:
                rating = int(rating_input)
                if not (1 <= rating <= 10):
                    print("Rating must be between 1 and 10.")
                    return
            except ValueError:
                print("Rating must be a number.")
                return
        
        success = selected_visitor.add_visit(selected_poi.get_id(), date, rating)
        if success:
            print(f"Visit added successfully: {selected_visitor.get_name()} visited {selected_poi.get_name()}")
        else:
            print("Failed to add visit. Check date format (dd/mm/yyyy).")

    def list_all_visitors(self):
        visitors = self.system.get_visitors()
        if not visitors:
            print("No visitors found.")
            return
        
        print(f"\n{'Name':<20} {'Nationality':<15} {'Visits':<10} {'Unique POIs':<12}")
        print("-" * 60)
        for visitor in visitors:
            unique_pois = len(visitor.get_unique_visited_poi_ids())
            print(f"{visitor.get_name():<20} {visitor.get_nationality():<15} {visitor.get_num_visits():<10} {unique_pois:<12}")

    def view_visitor_details(self):
        visitors = self.system.get_visitors()
        if not visitors:
            print("No visitors available.")
            return
        
        print("Available visitors:")
        for i, visitor in enumerate(visitors, 1):
            print(f"{i}. {visitor.get_name()} ({visitor.get_nationality()})")
        
        try:
            choice = self.get_valid_int("Select visitor: ", 1, len(visitors))
            selected_visitor = visitors[choice - 1]
        except KeyboardInterrupt:
            return
        
        print(f"\n=== {selected_visitor.get_name()} Details ===")
        print(f"Nationality: {selected_visitor.get_nationality()}")
        print(f"Total visits: {selected_visitor.get_num_visits()}")
        print(f"Unique POIs visited: {len(selected_visitor.get_unique_visited_poi_ids())}")
        
        avg_rating = selected_visitor.get_average_rating()
        if avg_rating:
            print(f"Average rating: {avg_rating:.1f}")
        else:
            print("No ratings given")
        
        visits = selected_visitor.get_visits()
        if visits:
            print("\nVisit History:")
            print(f"{'POI Name':<25} {'Date':<12} {'Rating':<8}")
            print("-" * 50)
            
            pois_dict = {poi.get_id(): poi.get_name() for poi in self.system.get_pois()}
            
            for visit in visits:
                poi_name = pois_dict.get(visit['poi_id'], 'Unknown POI')
                rating = visit.get('rating', 'N/A')
                print(f"{poi_name:<25} {visit['date']:<12} {rating:<8}")

    # === POI QUERIES ===
    def poi_queries_submenu(self):
        while True:
            self.display_poi_queries_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_poi_queries_menu(choice)

    def handle_poi_queries_menu(self, choice: str):
        if choice == "1":
            self.list_pois_by_type()
        elif choice == "2":
            self.find_nearest_poi_pair()
        elif choice == "3":
            self.count_pois_per_type()
        elif choice == "4":
            self.query_pois_within_radius()
        elif choice == "5":
            self.query_k_closest_pois()
        elif choice == "6":
            self.query_boundary_pois()
        else:
            print("Invalid choice. Please try again.")

    def find_nearest_poi_pair(self):
        nearest = self.system.get_nearest_pois()
        if nearest:
            print(f"\nClosest POI pair:")
            print(f"  {nearest[0][1]} at {nearest[0][2]}")
            print(f"  {nearest[1][1]} at {nearest[1][2]}")
        else:
            print("No POIs found or insufficient POIs for comparison.")

    def count_pois_per_type(self):
        counts = self.system.get_num_pois_per_poi_type()
        print("\nPOIs per type:")
        if not counts:
            print("No POI types found.")
            return
            
        for poi_type, count in counts.items():
            print(f"  {poi_type}: {count}")

    def query_pois_within_radius(self):
        try:
            x = self.get_valid_float("Enter X coordinate: ")
            y = self.get_valid_float("Enter Y coordinate: ")
            r = self.get_valid_float("Enter radius: ", 0)
            
            pois = self.system.get_pois_within_distance(x, y, r)
            
            if pois:
                print(f"\nPOIs within {r} units of ({x}, {y}):")
                print(f"{'ID':<10} {'Name':<20} {'Coordinates':<15} {'Type':<15} {'Distance':<10}")
                print("-" * 80)
                for poi_id, name, coords, poi_type, distance in pois:
                    print(f"{poi_id:<10} {name:<20} {str(coords):<15} {poi_type:<15} {distance:.2f}")
            else:
                print("No POIs found within the specified radius.")
        
        except KeyboardInterrupt:
            return
    
    def query_k_closest_pois(self):
        try:
            x = self.get_valid_float("Enter X coordinate: ")
            y = self.get_valid_float("Enter Y coordinate: ")
            k = self.get_valid_int("Enter number of closest POIs (k): ", 1)
            
            pois = self.system.get_k_closest_pois(x, y, k)
            
            if pois:
                print(f"\n{k} closest POIs to ({x}, {y}):")
                print(f"{'ID':<10} {'Name':<20} {'Coordinates':<15} {'Type':<15} {'Distance':<10}")
                print("-" * 80)
                for poi_id, name, coords, poi_type, distance in pois:
                    print(f"{poi_id:<10} {name:<20} {str(coords):<15} {poi_type:<15} {distance:.2f}")
            else:
                print("No POIs found.")
        except KeyboardInterrupt:
            return

    def query_boundary_pois(self):
        try:
            x = self.get_valid_float("Enter X coordinate: ")
            y = self.get_valid_float("Enter Y coordinate: ")
            r = self.get_valid_float("Enter exact distance: ", 0)
            epsilon_input = input(f"Enter epsilon value (default {self.system.EPSILON}): ").strip()
            
            epsilon = None
            if epsilon_input:
                epsilon = float(epsilon_input)
            
            pois = self.system.get_pois_in_boundary(x, y, r, epsilon)
            
            if pois:
                print(f"\nPOIs at exactly {r} units from ({x}, {y}):")
                print(f"{'ID':<10} {'Name':<20} {'Coordinates':<15} {'Type':<15} {'Distance':<10}")
                print("-" * 80)
                for poi_id, name, coords, poi_type, distance in pois:
                    print(f"{poi_id:<10} {name:<20} {str(coords):<15} {poi_type:<15} {distance:.6f}")
            else:
                print(f"No POIs found at exactly distance {r}.")
        
        except ValueError:
            print("Error: Please enter valid numbers.")
        except KeyboardInterrupt:
            return

    # === VISITOR ANALYTICS ===
    def visitor_analytics_submenu(self):
        while True:
            self.display_visitor_analytics_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_visitor_analytics_menu(choice)

    def handle_visitor_analytics_menu(self, choice: str):
        if choice == "1":
            self.visitor_poi_history()
        elif choice == "2":
            self.visitors_per_poi()
        elif choice == "3":
            self.pois_per_visitor()
        elif choice == "4":
            self.most_active_visitors()
        elif choice == "5":
            self.most_popular_pois()
        elif choice == "6":
            self.coverage_fairness_analysis()
        else:
            print("Invalid choice. Please try again.")

    def visitor_poi_history(self):
        visitors = self.system.get_visitors()
        if not visitors:
            print("No visitors available.")
            return
            
        print("Available visitors:")
        for i, visitor in enumerate(visitors, 1):
            print(f"{i}. {visitor.get_name()}")
        
        try:
            choice = self.get_valid_int("Select visitor: ", 1, len(visitors))
            selected_visitor = visitors[choice - 1]
        except KeyboardInterrupt:
            return
        
        visits = self.system.get_visited_pois(selected_visitor.get_name())
        
        if visits:
            print(f"\n{selected_visitor.get_name()}'s visit history:")
            print(f"{'POI Name':<25} {'Date':<12}")
            print("-" * 40)
            for poi_id, name, date in visits:
                print(f"{name:<25} {date:<12}")
        else:
            print(f"{selected_visitor.get_name()} has no recorded visits.")

    def visitors_per_poi(self):
        poi_visitor_counts = self.system.get_num_visitors_per_poi()
        
        if not poi_visitor_counts:
            print("No POI visitor data available.")
            return
            
        print("\nVisitors per POI:")
        print(f"{'POI Name':<25} {'Visitor Count':<15}")
        print("-" * 45)
        
        pois_dict = {poi.get_id(): poi.get_name() for poi in self.system.get_pois()}
        
        # Sort by visitor count (descending), then by POI ID
        sorted_counts = sorted(poi_visitor_counts, key=lambda x: (-x[1], x[0]))
        
        for poi_id, count in sorted_counts:
            poi_name = pois_dict.get(poi_id, f"Unknown POI ({poi_id})")
            print(f"{poi_name:<25} {count:<15}")

    def pois_per_visitor(self):
        visitor_poi_counts = self.system.get_num_pois_per_visitor()
        
        if not visitor_poi_counts:
            print("No visitor POI data available.")
            return
            
        print("\nPOIs per visitor:")
        print(f"{'Visitor Name':<25} {'POI Count':<15}")
        print("-" * 45)
        
        visitors_dict = {visitor.get_id(): visitor.get_name() for visitor in self.system.get_visitors()}
        
        # Sort by POI count (descending), then by visitor ID
        sorted_counts = sorted(visitor_poi_counts, key=lambda x: (-x[1], x[0]))
        
        for visitor_id, count in sorted_counts:
            visitor_name = visitors_dict.get(visitor_id, f"Unknown Visitor ({visitor_id})")
            print(f"{visitor_name:<25} {count:<15}")

    def most_active_visitors(self):
        try:
            k = self.get_valid_int("Enter number of top visitors (k): ", 1)
            active_visitors = self.system.get_most_visited_k_visitors(k)
            
            if active_visitors:
                print(f"\nTop {k} most active visitors:")
                print(f"{'Visitor Name':<25} {'Total Visits':<15}")
                print("-" * 45)
                
                visitors_dict = {visitor.get_id(): visitor for visitor in self.system.get_visitors()}
                
                for visitor_id, name in active_visitors:
                    visitor_obj = visitors_dict.get(visitor_id)
                    visits_count = visitor_obj.get_num_visits() if visitor_obj else 0
                    print(f"{name:<25} {visits_count:<15}")
            else:
                print("No visitor data available.")
                
        except KeyboardInterrupt:
            return

    def most_popular_pois(self):
        try:
            k = self.get_valid_int("Enter number of top POIs (k): ", 1)
            popular_pois = self.system.get_crowdest_k_pois(k)
            
            if popular_pois:
                print(f"\nTop {k} most popular POIs:")
                print(f"{'POI Name':<25} {'Visitor Count':<15}")
                print("-" * 45)
                
                poi_visitor_counts = dict(self.system.get_num_visitors_per_poi())
                
                for poi_id, name in popular_pois:
                    visitor_count = poi_visitor_counts.get(poi_id, 0)
                    print(f"{name:<25} {visitor_count:<15}")
            else:
                print("No POI data available.")
                
        except KeyboardInterrupt:
            return

    def coverage_fairness_analysis(self):
        try:
            m = self.get_valid_int("Enter minimum number of POIs visited (m): ", 1)
            t = self.get_valid_int("Enter minimum number of distinct POI types (t): ", 1)
            
            special_visitors = self.system.get_special_visitors(m, t)
            
            if special_visitors:
                print(f"\nVisitors with ≥{m} POI visits across ≥{t} distinct types:")
                print(f"{'Name':<20} {'Nationality':<15} {'Total POIs':<12} {'Distinct Types':<15}")
                print("-" * 70)
                
                for visitor_id, name, nationality, total_pois, distinct_types in special_visitors:
                    print(f"{name:<20} {nationality:<15} {total_pois:<12} {distinct_types:<15}")
            else:
                print(f"No visitors found with ≥{m} POI visits across ≥{t} distinct types.")
                
        except KeyboardInterrupt:
            return

    # === SYSTEM INFORMATION ===
    def system_information_submenu(self):
        while True:
            self.display_system_info_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_system_info_menu(choice)

    def handle_system_info_menu(self, choice: str):
        if choice == "1":
            self.show_overall_statistics()
        elif choice == "2":
            self.show_poi_type_details()
        elif choice == "3":
            self.show_map_boundary_info()
        elif choice == "4":
            self.quick_system_overview()
        else:
            print("Invalid choice. Please try again.")

    def show_overall_statistics(self):
        poi_types = self.system.get_poi_types()
        pois = self.system.get_pois()
        visitors = self.system.get_visitors()
        
        print("\n=== SYSTEM STATISTICS ===")
        print(f"Total POI Types: {len(poi_types)}")
        print(f"Total POIs: {len(pois)}")
        print(f"Total Visitors: {len(visitors)}")
        
        # Calculate total visits
        total_visits = sum(visitor.get_num_visits() for visitor in visitors)
        print(f"Total Visits: {total_visits}")
        
        # Average visits per visitor
        avg_visits = total_visits / len(visitors) if visitors else 0
        print(f"Average visits per visitor: {avg_visits:.1f}")
        
        # POI coverage
        visited_pois = set()
        for visitor in visitors:
            visited_pois.update(visitor.get_visited_poi_ids())
        
        coverage_percentage = (len(visited_pois) / len(pois) * 100) if pois else 0
        print(f"POI Coverage: {len(visited_pois)}/{len(pois)} ({coverage_percentage:.1f}%)")

    def show_poi_type_details(self):
        poi_types = self.system.get_poi_types()
        
        if not poi_types:
            print("No POI types available.")
            return
            
        print("\n=== POI TYPE DETAILS ===")
        for poi_type, info in poi_types.items():
            print(f"\n{poi_type}:")
            print(f"  POI Count: {info['num_pois']}")
            print(f"  Attributes: {', '.join(info['attributes']) if info['attributes'] else 'None'}")

    def show_map_boundary_info(self):
        pois = self.system.get_pois()
        
        print("\n=== MAP BOUNDARY INFORMATION ===")
        print("Map Size: 1000 x 1000 grid")
        print("Coordinate System: Integer coordinates (0,0) to (1000,1000)")
        
        if not pois:
            print("No POIs to analyze.")
            return
            
        # Calculate POI distribution
        x_coords = [poi.get_x() for poi in pois]
        y_coords = [poi.get_y() for poi in pois]
        
        print(f"\nPOI Distribution:")
        print(f"  X-range: {min(x_coords):.1f} to {max(x_coords):.1f}")
        print(f"  Y-range: {min(y_coords):.1f} to {max(y_coords):.1f}")
        print(f"  Center of mass: ({sum(x_coords)/len(x_coords):.1f}, {sum(y_coords)/len(y_coords):.1f})")

    # === CONFIGURATION MANAGEMENT ===
    def config_management_submenu(self):
        while True:
            self.display_config_menu()
            choice = input("\nEnter your choice: ").strip()
            if choice == "0":
                break
            self.handle_config_menu(choice)

    def handle_config_menu(self, choice: str):
        if choice == "1":
            self.load_config_file()
        elif choice == "2":
            self.save_current_state()
        elif choice == "3":
            self.system_validation_report()
        else:
            print("Invalid choice. Please try again.")

    def load_config_file(self):
        config_path = input("Enter configuration file path: ").strip()
        
        if not config_path:
            print("No file path provided.")
            return
            
        try:
            new_system = PoiManagementSystem(config_path)
            
            # Ask user if they want to replace current system
            print(f"Loaded: {len(new_system.get_poi_types())} POI types, "
                  f"{len(new_system.get_pois())} POIs, "
                  f"{len(new_system.get_visitors())} visitors")
            
            replace = input("Replace current system with loaded data? (y/N): ").strip().lower()
            if replace == 'y':
                self.system = new_system
                print("System replaced with loaded configuration.")
            else:
                print("Load cancelled.")
                
        except Exception as e:
            print(f"Error loading configuration: {e}")

    def save_current_state(self):
        print("Current system state:")
        print(f"  POI Types: {len(self.system.get_poi_types())}")
        print(f"  POIs: {len(self.system.get_pois())}")
        print(f"  Visitors: {len(self.system.get_visitors())}")
        print("\nNote: Save functionality would export to YAML format")
        print("(Implementation depends on specific requirements)")

    def system_validation_report(self):
        print("\n=== SYSTEM VALIDATION REPORT ===")
        
        # Check for orphaned data
        pois = self.system.get_pois()
        poi_types = self.system.get_poi_types()
        visitors = self.system.get_visitors()
        
        print(f"✓ Total POI Types: {len(poi_types)}")
        print(f"✓ Total POIs: {len(pois)}")
        print(f"✓ Total Visitors: {len(visitors)}")
        
        # Validate POI-POI Type consistency
        orphaned_pois = []
        for poi in pois:
            if poi.get_poi_type() not in poi_types:
                orphaned_pois.append(poi.get_name())
        
        if orphaned_pois:
            print(f"⚠ Orphaned POIs (missing POI type): {len(orphaned_pois)}")
            for poi_name in orphaned_pois[:5]:  # Show first 5
                print(f"    - {poi_name}")
            if len(orphaned_pois) > 5:
                print(f"    ... and {len(orphaned_pois) - 5} more")
        else:
            print("✓ All POIs have valid POI types")
        
        # Validate visitor visits
        valid_poi_ids = {poi.get_id() for poi in pois}
        invalid_visits = 0
        
        for visitor in visitors:
            for visit in visitor.get_visits():
                if visit['poi_id'] not in valid_poi_ids:
                    invalid_visits += 1
        
        if invalid_visits > 0:
            print(f"⚠ Invalid visitor visits (POI not found): {invalid_visits}")
        else:
            print("✓ All visitor visits reference valid POIs")
        
        # Coordinate validation
        invalid_coords = []
        for poi in pois:
            x, y = poi.get_coordinates()
            if not (0 <= x <= 1000 and 0 <= y <= 1000):
                invalid_coords.append(poi.get_name())
        
        if invalid_coords:
            print(f"⚠ POIs with invalid coordinates: {len(invalid_coords)}")
        else:
            print("✓ All POIs have valid coordinates (0-1000)")

    def view_all_poi_types(self):
        """Display all POI types with their attributes and POI counts"""
        poi_types = self.system.get_poi_types()
        
        if not poi_types:
            print("No POI types available.")
            return
        
        print(f"\n=== ALL POI TYPES ({len(poi_types)}) ===")
        print(f"{'Type':<20} {'POI Count':<10} {'Attributes'}")
        print("-" * 80)
        
        # Sort POI types alphabetically
        for poi_type in sorted(poi_types.keys()):
            info = poi_types[poi_type]
            attributes_str = ", ".join(info['attributes']) if info['attributes'] else "None"
            
            # Truncate long attribute lists
            if len(attributes_str) > 45:
                attributes_str = attributes_str[:42] + "..."
                
            print(f"{poi_type:<20} {info['num_pois']:<10} {attributes_str}")
        
        print()

    def view_all_pois(self):
        """Display all POIs in a formatted table"""
        pois = self.system.get_pois()
        
        if not pois:
            print("No POIs available.")
            return
        
        print(f"\n=== ALL POIs ({len(pois)}) ===")
        
        # Option to filter by POI type
        filter_choice = input("Filter by POI type? (Enter type name or press Enter for all): ").strip()
        
        if filter_choice:
            pois = [poi for poi in pois if poi.get_poi_type().lower() == filter_choice.lower()]
            if not pois:
                print(f"No POIs found for type '{filter_choice}'.")
                return
            print(f"Showing {len(pois)} POIs of type '{filter_choice}':")
        
        print(f"\n{'ID':<12} {'Name':<25} {'Type':<15} {'Coordinates':<15} {'Attributes'}")
        print("-" * 95)
        
        # Sort POIs by name
        sorted_pois = sorted(pois, key=lambda p: p.get_name())
        
        for poi in sorted_pois:
            # Format attributes for display
            attrs = poi.get_attributes()
            if attrs:
                # Show first few key-value pairs
                attr_items = list(attrs.items())[:2]
                attrs_str = ", ".join([f"{k}={v}" for k, v in attr_items])
                if len(attrs) > 2:
                    attrs_str += f" (+{len(attrs)-2} more)"
            else:
                attrs_str = "None"
            
            # Truncate if too long
            if len(attrs_str) > 25:
                attrs_str = attrs_str[:22] + "..."
            
            coords_str = f"({poi.get_x()}, {poi.get_y()})"
            
            print(f"{poi.get_id():<12} {poi.get_name():<25} {poi.get_poi_type():<15} {coords_str:<15} {attrs_str}")
        
        print()

    def view_all_visitors_detailed(self):
        """Display all visitors with detailed information"""
        visitors = self.system.get_visitors()
        
        if not visitors:
            print("No visitors available.")
            return
        
        print(f"\n=== ALL VISITORS - DETAILED VIEW ({len(visitors)}) ===")
        
        # Sort visitors by name
        sorted_visitors = sorted(visitors, key=lambda v: v.get_name())
        
        for visitor in sorted_visitors:
            print(f"\n📍 {visitor.get_name()} ({visitor.get_nationality()})")
            print(f"   ID: {visitor.get_id()}")
            print(f"   Total visits: {visitor.get_num_visits()}")
            print(f"   Unique POIs: {len(visitor.get_unique_visited_poi_ids())}")
            
            avg_rating = visitor.get_average_rating()
            if avg_rating:
                print(f"   Average rating: {avg_rating:.1f}/10")
            else:
                print(f"   Average rating: No ratings given")
            
            # Show recent visits (last 3)
            visits = visitor.get_visits()
            if visits:
                print("   Recent visits:")
                
                # Get POI names for visits
                pois_dict = {poi.get_id(): poi.get_name() for poi in self.system.get_pois()}
                
                # Show last 3 visits
                recent_visits = visits[-3:] if len(visits) > 3 else visits
                
                for visit in recent_visits:
                    poi_name = pois_dict.get(visit['poi_id'], 'Unknown POI')
                    rating_str = f" (★{visit['rating']})" if visit.get('rating') else ""
                    print(f"     • {poi_name} on {visit['date']}{rating_str}")
                
                if len(visits) > 3:
                    print(f"     ... and {len(visits) - 3} more visits")
            else:
                print("   No visits recorded")
        
        print()

    def quick_system_overview(self):
        """Quick overview of the entire system"""
        poi_types = self.system.get_poi_types()
        pois = self.system.get_pois()
        visitors = self.system.get_visitors()
        
        print("\n" + "="*50)
        print("           QUICK SYSTEM OVERVIEW")
        print("="*50)
        
        # Basic counts
        print(f"📍 POI Types: {len(poi_types)}")
        print(f"🏢 POIs: {len(pois)}")
        print(f"👥 Visitors: {len(visitors)}")
        
        if not pois and not visitors:
            print("\nSystem is empty. Load a configuration or add data manually.")
            return
        
        # POI Types summary
        if poi_types:
            print(f"\n📋 POI Types:")
            for poi_type, info in sorted(poi_types.items()):
                print(f"   • {poi_type}: {info['num_pois']} POIs")
        
        # Top POIs by visits
        if visitors and pois:
            poi_visit_counts = {}
            pois_dict = {poi.get_id(): poi.get_name() for poi in pois}
            
            for visitor in visitors:
                for poi_id in visitor.get_visited_poi_ids():
                    poi_visit_counts[poi_id] = poi_visit_counts.get(poi_id, 0) + 1
            
            if poi_visit_counts:
                print(f"\n🔥 Most Popular POIs:")
                sorted_pois = sorted(poi_visit_counts.items(), key=lambda x: x[1], reverse=True)
                for poi_id, count in sorted_pois[:3]:
                    poi_name = pois_dict.get(poi_id, 'Unknown')
                    print(f"   • {poi_name}: {count} visits")
        
        # Most active visitors
        if visitors:
            print(f"\n⭐ Most Active Visitors:")
            sorted_visitors = sorted(visitors, key=lambda v: v.get_num_visits(), reverse=True)
            for visitor in sorted_visitors[:3]:
                unique_pois = len(visitor.get_unique_visited_poi_ids())
                print(f"   • {visitor.get_name()}: {visitor.get_num_visits()} visits to {unique_pois} POIs")
        
        # Map coverage
        if pois:
            x_coords = [poi.get_x() for poi in pois]
            y_coords = [poi.get_y() for poi in pois]
            print(f"\n🗺️  Map Coverage:")
            print(f"   X-range: {min(x_coords):.0f} - {max(x_coords):.0f}")
            print(f"   Y-range: {min(y_coords):.0f} - {max(y_coords):.0f}")
        
        print("="*50)

    def view_poi_details(self):
        """View detailed information about a specific POI"""
        pois = self.system.get_pois()
        if not pois:
            print("No POIs available.")
            return
        
        print("Available POIs:")
        for i, poi in enumerate(pois, 1):
            print(f"{i}. {poi.get_name()} ({poi.get_poi_type()})")
        
        try:
            choice = self.get_valid_int("Select POI for details: ", 1, len(pois))
            selected_poi = pois[choice - 1]
        except KeyboardInterrupt:
            return
        
        print(f"\n=== {selected_poi.get_name()} Details ===")
        print(f"ID: {selected_poi.get_id()}")
        print(f"Type: {selected_poi.get_poi_type()}")
        print(f"Coordinates: {selected_poi.get_coordinates()}")
        
        attributes = selected_poi.get_attributes()
        if attributes:
            print("Attributes:")
            for key, value in attributes.items():
                print(f"  • {key}: {value}")
        else:
            print("Attributes: None")
        
        # Show visitor statistics for this POI
        visitors_to_this_poi = []
        for visitor in self.system.get_visitors():
            visits = visitor.get_visits_to_poi(selected_poi.get_id())
            if visits:
                visitors_to_this_poi.extend([(visitor.get_name(), visit) for visit in visits])
        
        if visitors_to_this_poi:
            print(f"\nVisitor History ({len(visitors_to_this_poi)} visits):")
            print(f"{'Visitor':<20} {'Date':<12} {'Rating'}")
            print("-" * 40)
            
            # Sort by date (most recent first)
            for visitor_name, visit in visitors_to_this_poi:
                rating = visit.get('rating', 'N/A')
                print(f"{visitor_name:<20} {visit['date']:<12} {rating}")
        else:
            print("\nNo visitors have visited this POI yet.")


def main():
    """Entry point for the CLI application"""
    parser = argparse.ArgumentParser(
        description="YAPOIMS - Yet Another POI Management System"
    )
    parser.add_argument(
        "-c", "--config", 
        help="Path to configuration file (YAML)",
        type=str,
        default=None
    )
    parser.add_argument(
        "--demo",
        help="Run with demo data",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Determine config file
    config_file = None
    if args.demo:
        import os
        config_file = os.path.join(os.path.dirname(__file__), '..', 'configs', 'sample.yaml')
    elif args.config:
        config_file = args.config
    
    try:
        cli = PoiManagementCLI(config_file)
        cli.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()