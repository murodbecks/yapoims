import re
from datetime import datetime
from typing import Dict, Optional, List, Union, Any

from yapoims.utils import check_type

class Visitor:
    """
    Represents a visitor in the POI Management System.
    
    A visitor is a person who can visit various Points of Interest (POIs).
    Each visitor has immutable core properties and maintains a record of all
    their visits with dates and optional ratings.
    
    Attributes:
        id (str): Unique identifier for the visitor (immutable)
        name (str): Full name of the visitor (immutable)  
        nationality (str): Nationality of the visitor (immutable)
        visits (list): List of visit records with POI IDs, dates, and ratings (modifiable)
    
    Each visit record is a dictionary containing:
        - poi_id: Identifier of the visited POI
        - date: Visit date in dd/mm/yyyy format
        - rating: Optional integer rating from 1-10
    """
    
    def __init__(self, id: str, name: str, nationality: str, visits: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Initialize a new Visitor instance.
        
        Args:
            id: Unique identifier for the visitor
            name: Full name of the visitor
            nationality: Nationality of the visitor
            visits: Optional list of visit dictionaries to initialize with
            
        Note:
            Invalid visits in the input list are filtered out during initialization.
            Each visit must have 'poi_id' and 'date' fields, with optional 'rating'.
        """
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "nationality", nationality)
        visits = visits or []
        # Filter out invalid visits during initialization
        valid_visits = []
        for visit in visits:
            verified = self._verify_visit(visit)
            if verified is not None:
                valid_visits.append(verified)
        object.__setattr__(self, "visits", valid_visits)
    
    # Getter methods
    def get_id(self) -> str:
        """Return the unique identifier of the visitor."""
        return self.id
    
    def get_name(self) -> str:
        """Return the name of the visitor."""
        return self.name
    
    def get_nationality(self) -> str:
        """Return the nationality of the visitor."""
        return self.nationality
    
    def get_visits(self) -> List[Dict[str, Any]]:
        """
        Return the list of all visits made by this visitor.
        
        Returns:
            A list of visit dictionaries, each containing poi_id, date, and optional rating.
        """
        return self.visits.copy()
    
    def get_num_visits(self) -> int:
        """
        Return the total number of visits made by this visitor.
        
        Returns:
            The count of all recorded visits (includes multiple visits to the same POI).
        """
        return len(self.get_visits())
    
    def get_visited_poi_ids(self) -> List[str]:
        """
        Return a list of all POI IDs that this visitor has visited.
        
        Returns:
            A list of POI identifiers. May contain duplicates if the visitor
            visited the same POI multiple times.
        """
        return [visit['poi_id'] for visit in self.get_visits()]
    
    def get_unique_visited_poi_ids(self) -> List[str]:
        """
        Return a list of unique POI IDs that this visitor has visited.
        
        Returns:
            A list of unique POI identifiers (no duplicates).
        """
        return list(set(self.get_visited_poi_ids()))
    
    def has_visited_poi(self, poi_id: str) -> bool:
        """
        Check if this visitor has ever visited a specific POI.
        
        Args:
            poi_id: The identifier of the POI to check
            
        Returns:
            True if the visitor has visited this POI at least once, False otherwise.
        """
        return poi_id in self.get_visited_poi_ids()

    # Private validation methods
    def _is_valid_date(self, date_str: str) -> bool:
        """
        Validate date format and value.
        
        Args:
            date_str: Date string to validate
            
        Returns:
            True if the date is in valid dd/mm/yyyy format and represents a real date.
        """
        if not isinstance(date_str, str):
            return False
            
        # Check format with regex
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_str):
            return False
        
        # Check if it's a valid date
        try:
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False
        
    def _verify_visit(self, visit: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Validate and clean a visit record.
        
        Args:
            visit: Dictionary containing visit information
            
        Returns:
            A cleaned visit dictionary with valid fields only, or None if invalid.
        """
        if not isinstance(visit, dict):
            return None
        
        clean_visit = {}
        
        # Validate poi_id (required)
        if 'poi_id' not in visit:
            return None
        poi_id = visit['poi_id']
        if not isinstance(poi_id, (int, str)):
            return None
        clean_visit['poi_id'] = poi_id
        
        # Validate date (required)
        if 'date' not in visit:
            return None
        date_str = visit['date']
        if not isinstance(date_str, str) or not self._is_valid_date(date_str):
            return None
        clean_visit['date'] = date_str
        
        # Validate rating (optional)
        rating = visit.get('rating')
        if rating is not None:
            if isinstance(rating, int) and 1 <= rating <= 10:
                clean_visit['rating'] = rating
            else:
                clean_visit['rating'] = None
        else:
            clean_visit['rating'] = None
        
        return clean_visit

    # Visit management methods
    def add_visit(self, poi_id: str, date: str, rating: Optional[int] = None) -> bool:
        """
        Add a new visit record for this visitor.
        
        Args:
            poi_id: Identifier of the visited POI
            date: Visit date in dd/mm/yyyy format
            rating: Optional rating from 1-10
            
        Returns:
            True if the visit was successfully added, False if validation failed.
        """
        verified_visit = self._verify_visit({
            'poi_id': poi_id, 
            'date': date, 
            'rating': rating
        })

        if verified_visit is not None:
            all_visits = self.get_visits()
            all_visits.append(verified_visit)
            object.__setattr__(self, "visits", all_visits)
            return True
        else:
            print('Invalid visit data - please check poi_id, date format (dd/mm/yyyy), and rating (1-10)')
            return False
    
    def delete_visit(self, poi_id: str) -> bool:
        check_type(poi_id, str, "poi_id")
        
        all_visits = self.get_visits()
        
        poi_idx_to_delete = None

        for i, visit in enumerate(all_visits):
            if visit['poi_id'] == poi_id:
                poi_idx_to_delete = i
                break
        
        if poi_idx_to_delete is None:
            print(f"Warning: Trying to delete non-existent POI id: {poi_id}")
            return False
        else:
            all_visits.pop(poi_idx_to_delete)
            object.__setattr__(self, "visits", all_visits)
            return True
    
    def get_visits_to_poi(self, poi_id: str) -> List[Dict[str, Any]]:
        """
        Get all visits made by this visitor to a specific POI.
        
        Args:
            poi_id: The identifier of the POI
            
        Returns:
            A list of visit records for the specified POI.
        """
        return [visit for visit in self.get_visits() if visit['poi_id'] == poi_id]
    
    def get_average_rating(self) -> Optional[float]:
        """
        Calculate the average rating given by this visitor across all rated visits.
        
        Returns:
            The average rating as a float, or None if no visits have ratings.
        """
        rated_visits = [visit for visit in self.get_visits() if visit.get('rating') is not None]
        if not rated_visits:
            return None
        return sum(visit['rating'] for visit in rated_visits) / len(rated_visits)

    # Special methods (dunder methods)
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the visitor.
        
        Returns:
            A string showing all visitor properties in a readable format.
        """
        return (f"Visitor(id='{self.get_id()}', name='{self.get_name()}', "
                f"nationality='{self.get_nationality()}', visits={self.get_visits()})")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent direct attribute modification after initialization.
        
        Raises:
            AttributeError: Always, to maintain immutability of core properties
        """
        raise AttributeError(f"Cannot set attribute '{name}' - use provided methods instead")
    
    def __delattr__(self, name: str) -> None:
        """
        Prevent attribute deletion.
        
        Raises:
            AttributeError: Always, to maintain object integrity
        """
        raise AttributeError(f"Cannot delete attribute '{name}' - visitor properties are protected")
    
    def __eq__(self, other: object) -> bool:
        """
        Compare two Visitor objects for equality.
        
        Args:
            other: Another object to compare against
            
        Returns:
            True if both objects are Visitors with identical properties, False otherwise
            
        Note:
            Two visitors are considered equal if ALL their properties match exactly,
            including all visit records.
        """
        if not isinstance(other, Visitor):
            return False
        
        return (self.get_id(), self.get_name(), self.get_nationality(), self.get_visits()) == \
               (other.get_id(), other.get_name(), other.get_nationality(), other.get_visits())


if __name__ == "__main__":
    print("=== POI Management System - Visitor Class Demo ===\n")
    
    # Test 1: Creating visitors with mixed valid/invalid data
    print("1. Creating visitors with sample visit data...")
    visitor1 = Visitor('V001', 'Alice Johnson', 'American', [
        {'poi_id': 'P001', 'date': '19/09/2024'},  # Valid
        {'poi_id': 'P002', 'date': '01/07/2024', 'ratings': 4},  # Invalid key 'ratings'
        {'poi_id': 'P003', 'dates': '01/07/2024', 'rating': 4},  # Invalid key 'dates'  
        {'poi_id': 'P004', 'date': '15/08/2024', 'rating': 7}  # Valid
    ])
    
    visitor2 = Visitor('V002', 'Bob Garcia', 'Spanish', [
        {'poi_id': 'P002', 'date': '19/09/2024', 'rating': '4'},  # Invalid rating type
        {'poi_id': 'P001', 'rating': 7},  # Missing date
        {'poi_id': 'P005', 'date': '20/09/2024', 'rating': 9}  # Valid
    ])
    
    # Create visitor with no initial visits
    visitor3 = Visitor('V003', 'Carol Kim', 'Korean')
    
    print(f"Visitor-1 (Alice): {visitor1.get_num_visits()} valid visits")
    print(f"Visitor-2 (Bob): {visitor2.get_num_visits()} valid visits") 
    print(f"Visitor-3 (Carol): {visitor3.get_num_visits()} visits")
    print()

    # Test 2: Equality testing
    print("2. Testing visitor equality...")
    visitor1_copy = Visitor('V001', 'Alice Johnson', 'American', [
        {'poi_id': 'P001', 'date': '19/09/2024'},
        {'poi_id': 'P004', 'date': '15/08/2024', 'rating': 7}
    ])
    
    print(f"visitor1 == visitor1: {visitor1 == visitor1}")
    print(f"visitor1 == visitor2: {visitor1 == visitor2}")
    print(f"visitor1 == visitor1_copy: {visitor1 == visitor1_copy}")
    print(f"visitor1 == 'not a visitor': {visitor1 == 'not a visitor'}")
    print()

    # Test 3: Visit information queries
    print("3. Querying visit information...")
    print(f"Alice visited POI IDs: {visitor1.get_visited_poi_ids()}")
    print(f"Alice unique POI IDs: {visitor1.get_unique_visited_poi_ids()}")
    print(f"Alice has visited P001: {visitor1.has_visited_poi('P001')}")
    print(f"Alice has visited P999: {visitor1.has_visited_poi('P999')}")
    print(f"Alice's average rating: {visitor1.get_average_rating()}")
    print()

    # Test 4: Adding new visits
    print("4. Testing visit addition...")
    print(f"Carol before adding visits: {visitor3.get_num_visits()} visits")
    
    # Add valid visit
    success1 = visitor3.add_visit('P001', '22/09/2024', 8)
    print(f"Added valid visit, success: {success1}")
    
    # Try to add invalid visit (bad date format)
    print("Attempting to add visit with invalid date:")
    success2 = visitor3.add_visit('P002', '2024-09-22', 9)  # Wrong date format
    print(f"Added invalid date visit, success: {success2}")
    
    # Try to add visit with invalid rating
    print("Attempting to add visit with invalid rating:")
    success3 = visitor3.add_visit('P003', '23/09/2024', 15)  # Rating > 10
    print(f"Added invalid rating visit, success: {success3}")
    
    print(f"Carol after adding visits: {visitor3.get_num_visits()} visits")
    print(f"Carol's visits: {visitor3.get_visits()}")
    print()

    # Test 5: Advanced queries
    print("5. Advanced visit queries...")
    
    # Add more visits to demonstrate advanced features
    visitor1.add_visit('P001', '25/09/2024', 9)  # Revisit P001
    visitor1.add_visit('P006', '26/09/2024', 6)
    
    print(f"Alice total visits: {visitor1.get_num_visits()}")
    print(f"Alice unique POIs visited: {len(visitor1.get_unique_visited_poi_ids())}")
    print(f"Alice visits to P001: {visitor1.get_visits_to_poi('P001')}")
    print(f"Alice current average rating: {visitor1.get_average_rating():.2f}")
    print()

    # Test 6: Edge cases and validation
    print("6. Testing edge cases...")
    
    # Test date validation edge cases
    edge_visitor = Visitor('V999', 'Edge Case', 'Unknown')
    
    test_cases = [
        ('P001', '29/02/2024', 5),  # Valid leap year
        ('P002', '29/02/2023', 5),  # Invalid leap year
        ('P003', '32/01/2024', 5),  # Invalid day
        ('P004', '01/13/2024', 5),  # Invalid month
        ('P005', '01/01/24', 5),    # Wrong year format
    ]
    
    print("Testing date validation:")
    for poi_id, date, rating in test_cases:
        success = edge_visitor.add_visit(poi_id, date, rating)
        print(f"  Date '{date}': {'✓' if success else '✗'}")
    
    print(f"Edge visitor valid visits: {edge_visitor.get_num_visits()}")
    
    # Test 7: Immutability
    print("\n7. Testing immutability...")
    try:
        visitor1.id = "new_id"
    except AttributeError as e:
        print(f"Expected error when trying to modify id: {e}")
    
    try:
        visitor1.name = "New Name"
    except AttributeError as e:
        print(f"Expected error when trying to modify name: {e}")
    
    print("\n=== Demo completed successfully! ===")