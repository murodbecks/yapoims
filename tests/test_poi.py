import pytest
from yapoims.poi import Poi


class TestPoiInitialization:
    """Test POI creation and initialization."""
    
    def test_poi_creation_basic(self):
        """Test creating a POI with basic information."""
        poi = Poi('P001', 'Test Museum', 'museum', 100, 200)
        
        assert poi.get_id() == 'P001'
        assert poi.get_name() == 'Test Museum'
        assert poi.get_poi_type() == 'museum'
        assert poi.get_x() == 100
        assert poi.get_y() == 200
        assert poi.get_attributes() == {}
    
    def test_poi_creation_with_attributes(self):
        """Test creating a POI with custom attributes."""
        attributes = {
            'opening_hours': '09:00-17:00',
            'entrance_fee': '25 AED',
            'wheelchair_accessible': True
        }
        poi = Poi('P001', 'Art Gallery', 'museum', 150, 250, attributes)
        
        assert poi.get_attributes() == attributes
        assert list(poi.get_attribute_names()) == list(attributes.keys())
    
    def test_poi_creation_with_float_coordinates(self):
        """Test creating a POI with float coordinates."""
        poi = Poi('P001', 'Beach Point', 'beach', 123.45, 678.90)
        
        assert poi.get_x() == 123.45
        assert poi.get_y() == 678.90
        assert poi.get_coordinates() == (123.45, 678.90)
    
    def test_poi_creation_none_attributes(self):
        """Test POI creation handles None attributes properly."""
        poi = Poi('P001', 'Simple POI', 'park', 50, 50, None)
        
        assert poi.get_attributes() == {}
        assert len(list(poi.get_attribute_names())) == 0


class TestPoiProperties:
    """Test POI property access methods."""
    
    @pytest.fixture
    def sample_poi(self):
        """Create a sample POI for testing."""
        attributes = {
            'capacity': '500',
            'parking_available': True,
            'rating': 4.5
        }
        return Poi('P001', 'Central Library', 'library', 300, 400, attributes)
    
    def test_get_coordinates(self, sample_poi):
        """Test getting coordinates as tuple."""
        coords = sample_poi.get_coordinates()
        assert coords == (300, 400)
        assert isinstance(coords, tuple)
    
    def test_get_attribute_names(self, sample_poi):
        """Test getting attribute names."""
        attr_names = list(sample_poi.get_attribute_names())
        expected_names = ['capacity', 'parking_available', 'rating']
        assert set(attr_names) == set(expected_names)
    
    def test_attributes_immutability(self, sample_poi):
        """Test that returned attributes dict doesn't affect internal state."""
        attrs = sample_poi.get_attributes()
        attrs['new_attribute'] = 'test_value'
        
        # Internal state should be unchanged
        assert 'new_attribute' not in sample_poi.get_attributes()
        assert len(sample_poi.get_attributes()) == 3


class TestPoiTypeModification:
    """Test POI type modification functionality."""
    
    def test_set_poi_type(self):
        """Test changing POI type."""
        poi = Poi('P001', 'Cultural Center', 'museum', 100, 200)
        
        assert poi.get_poi_type() == 'museum'
        poi.set_poi_type('cultural_center')
        assert poi.get_poi_type() == 'cultural_center'
    
    def test_set_poi_type_multiple_changes(self):
        """Test multiple POI type changes."""
        poi = Poi('P001', 'Multi-use Building', 'office', 100, 200)
        
        poi.set_poi_type('restaurant')
        assert poi.get_poi_type() == 'restaurant'
        
        poi.set_poi_type('shopping_mall')
        assert poi.get_poi_type() == 'shopping_mall'


class TestAttributeManagement:
    """Test POI attribute management methods."""
    
    @pytest.fixture
    def poi_with_attributes(self):
        """Create a POI with initial attributes."""
        initial_attrs = {
            'size': 'large',
            'established': '2020',
            'features': ['wifi', 'parking']
        }
        return Poi('P001', 'Test Venue', 'venue', 200, 300, initial_attrs)
    
    def test_add_attribute_new(self, poi_with_attributes):
        """Test adding a new attribute."""
        poi_with_attributes.add_attribute('opening_time', '08:00')
        
        attrs = poi_with_attributes.get_attributes()
        assert 'opening_time' in attrs
        assert attrs['opening_time'] == '08:00'
        assert len(attrs) == 4
    
    def test_add_attribute_update_existing(self, poi_with_attributes):
        """Test updating an existing attribute."""
        poi_with_attributes.add_attribute('size', 'medium')
        
        attrs = poi_with_attributes.get_attributes()
        assert attrs['size'] == 'medium'
        assert len(attrs) == 3  # Same number of attributes
    
    def test_add_attribute_none_value(self, poi_with_attributes):
        """Test adding attribute with None value."""
        poi_with_attributes.add_attribute('special_note')
        
        attrs = poi_with_attributes.get_attributes()
        assert 'special_note' in attrs
        assert attrs['special_note'] is None
    
    def test_delete_attribute_existing(self, poi_with_attributes):
        """Test deleting an existing attribute."""
        success = poi_with_attributes.delete_attribute('size')
        
        assert success is True
        attrs = poi_with_attributes.get_attributes()
        assert 'size' not in attrs
        assert len(attrs) == 2
    
    def test_delete_attribute_nonexistent(self, poi_with_attributes):
        """Test deleting a non-existent attribute."""
        success = poi_with_attributes.delete_attribute('nonexistent')
        
        assert success is False
        # Attributes should remain unchanged
        assert len(poi_with_attributes.get_attributes()) == 3
    
    def test_change_attribute_name_existing(self, poi_with_attributes):
        """Test renaming an existing attribute."""
        success = poi_with_attributes.change_attribute_name('size', 'dimensions')
        
        assert success is True
        attrs = poi_with_attributes.get_attributes()
        assert 'size' not in attrs
        assert 'dimensions' in attrs
        assert attrs['dimensions'] == 'large'  # Value preserved
    
    def test_change_attribute_name_nonexistent(self, poi_with_attributes):
        """Test renaming a non-existent attribute."""
        success = poi_with_attributes.change_attribute_name('nonexistent', 'new_name')
        
        assert success is False
        # Attributes should remain unchanged
        original_keys = set(poi_with_attributes.get_attributes().keys())
        assert original_keys == {'size', 'established', 'features'}


class TestPoiImmutability:
    """Test that POI core properties are immutable."""
    
    def test_cannot_modify_id(self):
        """Test that POI ID cannot be modified."""
        poi = Poi('P001', 'Test POI', 'test', 100, 200)
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'id'"):
            poi.id = 'P002'
    
    def test_cannot_modify_name(self):
        """Test that POI name cannot be modified."""
        poi = Poi('P001', 'Test POI', 'test', 100, 200)
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'name'"):
            poi.name = 'New Name'
    
    def test_cannot_modify_coordinates(self):
        """Test that POI coordinates cannot be modified."""
        poi = Poi('P001', 'Test POI', 'test', 100, 200)
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'x'"):
            poi.x = 999
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'y'"):
            poi.y = 999
    
    def test_cannot_delete_attributes(self):
        """Test that POI core attributes cannot be deleted."""
        poi = Poi('P001', 'Test POI', 'test', 100, 200)
        
        with pytest.raises(AttributeError, match="Cannot delete attribute 'id'"):
            del poi.id
        
        with pytest.raises(AttributeError, match="Cannot delete attribute 'name'"):
            del poi.name


class TestPoiEquality:
    """Test POI equality comparison."""
    
    def test_poi_equality_identical(self):
        """Test that identical POIs are equal."""
        attributes = {'type': 'outdoor', 'area': '100m²'}
        poi1 = Poi('P001', 'Park A', 'park', 100, 200, attributes)
        poi2 = Poi('P001', 'Park A', 'park', 100, 200, attributes)
        
        assert poi1 == poi2
        assert poi1 == poi1  # Self-equality
    
    def test_poi_equality_different_ids(self):
        """Test that POIs with different IDs are not equal."""
        poi1 = Poi('P001', 'Same POI', 'park', 100, 200)
        poi2 = Poi('P002', 'Same POI', 'park', 100, 200)
        
        assert poi1 != poi2
    
    def test_poi_equality_different_names(self):
        """Test that POIs with different names are not equal."""
        poi1 = Poi('P001', 'Park A', 'park', 100, 200)
        poi2 = Poi('P001', 'Park B', 'park', 100, 200)
        
        assert poi1 != poi2
    
    def test_poi_equality_different_coordinates(self):
        """Test that POIs with different coordinates are not equal."""
        poi1 = Poi('P001', 'Same POI', 'park', 100, 200)
        poi2 = Poi('P001', 'Same POI', 'park', 150, 200)
        
        assert poi1 != poi2
    
    def test_poi_equality_different_attributes(self):
        """Test that POIs with different attributes are not equal."""
        poi1 = Poi('P001', 'POI', 'park', 100, 200, {'size': 'large'})
        poi2 = Poi('P001', 'POI', 'park', 100, 200, {'size': 'small'})
        
        assert poi1 != poi2
    
    def test_poi_equality_after_modification(self):
        """Test equality after POI modification."""
        poi1 = Poi('P001', 'Museum', 'museum', 100, 200)
        poi2 = Poi('P001', 'Museum', 'museum', 100, 200)
        
        assert poi1 == poi2
        
        # Modify poi1
        poi1.set_poi_type('art_museum')
        assert poi1 != poi2  # Should no longer be equal
    
    def test_poi_equality_with_non_poi(self):
        """Test that POI is not equal to non-POI objects."""
        poi = Poi('P001', 'Test POI', 'test', 100, 200)
        
        assert poi != 'not a poi'
        assert poi != 123
        assert poi != None
        assert poi != {}
        assert poi != ['P001', 'Test POI']


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_poi_with_empty_string_values(self):
        """Test POI creation with empty string values."""
        poi = Poi('', '', '', 0, 0, {'empty': ''})
        
        assert poi.get_id() == ''
        assert poi.get_name() == ''
        assert poi.get_poi_type() == ''
        assert poi.get_attributes()['empty'] == ''
    
    def test_poi_with_extreme_coordinates(self):
        """Test POI creation with boundary coordinate values."""
        poi = Poi('P001', 'Boundary POI', 'test', 0, 1000)
        
        assert poi.get_coordinates() == (0, 1000)
        
        poi2 = Poi('P002', 'Another Boundary', 'test', 1000, 0)
        assert poi2.get_coordinates() == (1000, 0)
    
    def test_poi_with_complex_attributes(self):
        """Test POI with complex attribute values."""
        complex_attrs = {
            'nested_dict': {'level2': {'level3': 'deep_value'}},
            'list_attr': [1, 2, 3, 'mixed', True],
            'none_value': None,
            'boolean_attr': False,
            'numeric_attr': 42.5
        }
        poi = Poi('P001', 'Complex POI', 'complex', 500, 500, complex_attrs)
        
        retrieved_attrs = poi.get_attributes()
        assert retrieved_attrs['nested_dict']['level2']['level3'] == 'deep_value'
        assert retrieved_attrs['list_attr'] == [1, 2, 3, 'mixed', True]
        assert retrieved_attrs['none_value'] is None
        assert retrieved_attrs['boolean_attr'] is False
        assert retrieved_attrs['numeric_attr'] == 42.5
    
    def test_poi_representation(self):
        """Test POI string representation."""
        poi = Poi('P001', 'Test Museum', 'museum', 150, 250, {'fee': '20 AED'})
        
        repr_str = repr(poi)
        assert 'P001' in repr_str
        assert 'Test Museum' in repr_str
        assert 'museum' in repr_str
        assert '150' in repr_str
        assert '250' in repr_str
        assert 'fee' in repr_str
    
    def test_attribute_modification_chain(self):
        """Test chaining attribute modifications."""
        poi = Poi('P001', 'Chain Test', 'test', 100, 100)
        
        # Chain multiple attribute operations
        poi.add_attribute('attr1', 'value1')
        poi.add_attribute('attr2', 'value2')
        poi.change_attribute_name('attr1', 'renamed_attr1')
        poi.delete_attribute('attr2')
        
        attrs = poi.get_attributes()
        assert 'renamed_attr1' in attrs
        assert attrs['renamed_attr1'] == 'value1'
        assert 'attr1' not in attrs
        assert 'attr2' not in attrs
        assert len(attrs) == 1
    
    def test_coordinate_type_consistency(self):
        """Test that coordinate types are preserved."""
        poi_int = Poi('P001', 'Int Coords', 'test', 100, 200)
        poi_float = Poi('P002', 'Float Coords', 'test', 100.0, 200.0)
        poi_mixed = Poi('P003', 'Mixed Coords', 'test', 100, 200.5)
        
        assert isinstance(poi_int.get_x(), int)
        assert isinstance(poi_int.get_y(), int)
        assert isinstance(poi_float.get_x(), float)
        assert isinstance(poi_float.get_y(), float)
        assert isinstance(poi_mixed.get_x(), int)
        assert isinstance(poi_mixed.get_y(), float)


class TestAttributeEdgeCases:
    """Test edge cases in attribute management."""
    
    def test_add_attribute_overwrite_warning_suppression(self):
        """Test that adding attributes doesn't generate unnecessary warnings."""
        poi = Poi('P001', 'Test', 'test', 100, 100, {'existing': 'value'})
        
        # This should work silently (no warning expected for overwrite)
        poi.add_attribute('existing', 'new_value')
        assert poi.get_attributes()['existing'] == 'new_value'
    
    def test_delete_multiple_times(self):
        """Test deleting the same attribute multiple times."""
        poi = Poi('P001', 'Test', 'test', 100, 100, {'to_delete': 'value'})
        
        # First deletion should succeed
        assert poi.delete_attribute('to_delete') is True
        assert 'to_delete' not in poi.get_attributes()
        
        # Second deletion should fail
        assert poi.delete_attribute('to_delete') is False
    
    def test_rename_to_existing_key(self):
        """Test renaming attribute to an existing key name."""
        poi = Poi('P001', 'Test', 'test', 100, 100, {
            'attr1': 'value1',
            'attr2': 'value2'
        })
        
        # Rename attr1 to attr2 (which already exists)
        success = poi.change_attribute_name('attr1', 'attr2')
        
        assert success is True
        attrs = poi.get_attributes()
        assert 'attr1' not in attrs
        assert attrs['attr2'] == 'value1'  # attr1's value should overwrite attr2
        assert len(attrs) == 1