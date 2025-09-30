from typing import Union, Optional, Dict, Tuple, Any


class Poi:
    """
    Represents a Point of Interest (POI) on a map.
    
    A POI is a specific location with a name, type, coordinates, and custom attributes.
    Core properties (id, name, coordinates) are immutable after creation, but the POI
    type and attributes can be modified.
    
    Attributes:
        id (str): Unique identifier for the POI (immutable)
        name (str): Human-readable name of the POI (immutable)
        poi_type (str): Category/type of the POI (modifiable)
        x (Union[int, float]): X-coordinate on the map (immutable)
        y (Union[int, float]): Y-coordinate on the map (immutable)
        attributes (dict): Custom attributes specific to the POI type (modifiable)
    """
    
    def __init__(self, id: str, name: str, poi_type: str, x: Union[int, float], 
                 y: Union[int, float], attributes: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a new POI instance.
        
        Args:
            id: Unique identifier for the POI
            name: Human-readable name of the POI
            poi_type: Category/type of the POI (e.g., 'museum', 'park', 'restaurant')
            x: X-coordinate on the 1000x1000 grid
            y: Y-coordinate on the 1000x1000 grid
            attributes: Optional dictionary of custom attributes for this POI type
        """
        object.__setattr__(self, "id", id)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "poi_type", poi_type)
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "attributes", attributes or {})
    
    # Getter methods
    def get_id(self) -> str:
        """Return the unique identifier of the POI."""
        return self.id
    
    def get_name(self) -> str:
        """Return the name of the POI."""
        return self.name
    
    def get_poi_type(self) -> str:
        """Return the type/category of the POI."""
        return self.poi_type
    
    def get_x(self) -> Union[int, float]:
        """Return the X-coordinate of the POI."""
        return self.x
    
    def get_y(self) -> Union[int, float]:
        """Return the Y-coordinate of the POI."""
        return self.y
    
    def get_attributes(self) -> Dict[str, Any]:
        """
        Return the attributes dictionary of the POI.
        
        Returns:
            A dictionary containing all custom attributes for this POI.
        """
        return self.attributes.copy()
    
    def get_attribute_names(self) -> Tuple[str]:
        """
        Return the attribute names of the POI.
        
        Returns:
            A list containing all attribute names for this POI.
        """
        return list(self.attributes.keys())
    
    def get_coordinates(self) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Return the coordinates as a tuple.
        
        Returns:
            A tuple (x, y) representing the POI's location on the map.
        """
        return (self.get_x(), self.get_y())
    
    # Setter methods
    def set_poi_type(self, new_poi_type: str) -> None:
        """
        Change the POI type.
        
        Args:
            new_poi_type: The new type/category for this POI
        """
        object.__setattr__(self, "poi_type", new_poi_type)

    # Attribute management methods
    def add_attribute(self, attribute_key: str, attribute_value: Any = None) -> None:
        """
        Add or update an attribute for this POI.
        
        Args:
            attribute_key: The name of the attribute
            attribute_value: The value to assign (defaults to None)
        """
        attributes = self.get_attributes()
        attributes[attribute_key] = attribute_value
        object.__setattr__(self, "attributes", attributes)
    
    def delete_attribute(self, attribute_key: str) -> bool:
        """
        Remove an attribute from this POI.
        
        Args:
            attribute_key: The name of the attribute to remove
            
        Returns:
            True if the attribute was found and removed, False otherwise
        """
        attributes = self.get_attributes()
        
        if attribute_key in attributes:
            del attributes[attribute_key]
            object.__setattr__(self, "attributes", attributes)
            return True
        else:
            print(f"Warning: '{attribute_key}' not found in attributes")
            return False

    def change_attribute_name(self, old_key: str, new_key: str) -> bool:
        """
        Rename an attribute key while preserving its value.
        
        Args:
            old_key: The current name of the attribute
            new_key: The new name for the attribute
            
        Returns:
            True if the attribute was found and renamed, False otherwise
        """
        attributes = self.get_attributes()

        if old_key in attributes:
            attributes[new_key] = attributes.pop(old_key)
            object.__setattr__(self, "attributes", attributes)
            return True
        else:
            print(f"Warning: '{old_key}' not found in attributes")
            return False

    # Special methods (dunder methods)
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the POI.
        
        Returns:
            A string showing all POI properties in a readable format.
        """
        return (f"POI(id='{self.get_id()}', name='{self.get_name()}', "
                f"poi_type='{self.get_poi_type()}', x={self.get_x()}, "
                f"y={self.get_y()}, attributes={self.get_attributes()})")
    
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
        raise AttributeError(f"Cannot delete attribute '{name}' - POI properties are protected")
    
    def __eq__(self, other: object) -> bool:
        """
        Compare two POI objects for equality.
        
        Args:
            other: Another object to compare against
            
        Returns:
            True if both objects are POIs with identical properties, False otherwise
            
        Note:
            Two POIs are considered equal if ALL their properties match exactly.
        """
        if not isinstance(other, Poi):
            return False
        return (self.get_id(), self.get_name(), self.get_poi_type(), 
                self.get_x(), self.get_y(), self.get_attributes()) == \
               (other.get_id(), other.get_name(), other.get_poi_type(), 
                other.get_x(), other.get_y(), other.get_attributes())


if __name__ == "__main__":
    print("=== POI Management System - POI Class Demo ===\n")
    
    # Test 1: Creating POIs
    print("1. Creating sample POIs...")
    poi1 = Poi('01', 'Louvre Abu Dhabi', 'museum', 100, 200, 
               {'opening_hours': '10:00-18:00', 'entrance_fee': '63 AED'})
    poi2 = Poi('02', 'Central Park', 'park', 300, 400, 
               {'area_size': "50 hectares", 'pet_friendly': True})
    poi3 = Poi('01', 'Louvre Abu Dhabi', 'museum', 100, 200, 
               {'opening_hours': '10:00-18:00', 'entrance_fee': '63 AED'})  # Same as poi1
    
    print(f"POI-1: {poi1}")
    print(f"POI-2: {poi2}")
    print(f"POI-3: {poi3}")
    print()

    # Test 2: Equality testing
    print("2. Testing equality...")
    print(f"poi1 == poi1: {poi1 == poi1}")
    print(f"poi1 == poi2: {poi1 == poi2}")
    print(f"poi1 == poi3: {poi1 == poi3}")  # Should be True - identical content
    print(f"poi1 == 'not a poi': {poi1 == 'not a poi'}")  # Should be False
    print()

    # Test 3: Coordinate access
    print("3. Testing coordinate access...")
    print(f"POI-1 coordinates: {poi1.get_coordinates()}")
    print(f"POI-2 X: {poi2.get_x()}, Y: {poi2.get_y()}")
    print()

    # Test 4: POI type modification
    print("4. Testing POI type modification...")
    print(f"Before: {poi1.get_poi_type()}")
    poi1.set_poi_type('art_museum')
    print(f"After: {poi1.get_poi_type()}")
    print()

    # Test 5: Attribute management
    print("5. Testing attribute management...")
    print(f"Initial attributes: {poi1.get_attributes()}")
    
    # Add attribute
    poi1.add_attribute('exhibits', 'Modern Art Collection')
    print(f"After adding 'exhibits': {poi1.get_attributes()}")
    
    # Try to delete non-existent attribute
    print("Attempting to delete non-existent attribute:")
    success = poi1.delete_attribute("non_existent")
    print(f"Delete result: {success}")
    
    # Delete existing attribute
    print("Deleting 'entrance_fee' attribute:")
    success = poi1.delete_attribute("entrance_fee")
    print(f"Delete result: {success}")
    print(f"Attributes after deletion: {poi1.get_attributes()}")
    
    # Rename attribute
    print("Renaming 'opening_hours' to 'business_hours':")
    success = poi1.change_attribute_name('opening_hours', 'business_hours')
    print(f"Rename result: {success}")
    print(f"Final attributes: {poi1.get_attributes()}")
    print()

    # Test 6: Immutability testing
    print("6. Testing immutability...")
    try:
        poi1.id = "new_id"  # This should fail
    except AttributeError as e:
        print(f"Expected error when trying to modify id: {e}")
    
    try:
        poi1.x = 999  # This should fail
    except AttributeError as e:
        print(f"Expected error when trying to modify coordinates: {e}")
    
    print("\n=== Demo completed successfully! ===")