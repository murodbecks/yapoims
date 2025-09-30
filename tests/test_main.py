import pytest
import os
import tempfile
import yaml
from unittest.mock import patch
from yapoims.main import PoiManagementSystem
from yapoims.poi import Poi
from yapoims.visitor import Visitor
from yapoims.utils import ValueValidationError


class TestPoiManagementSystemInitialization:
    """Test PoiManagementSystem initialization and config loading."""
    
    def test_initialization_empty(self):
        """Test creating empty PoiManagementSystem."""
        poims = PoiManagementSystem()
        
        assert len(poims.get_poi_types()) == 0
        assert len(poims.get_pois()) == 0
        assert len(poims.get_visitors()) == 0
    
    def test_initialization_with_valid_config(self):
        """Test initialization with valid config file."""
        poims = PoiManagementSystem('configs/abu_dhabi.yaml')
        
        assert len(poims.get_poi_types()) > 0
        assert len(poims.get_pois()) > 0
        assert len(poims.get_visitors()) > 0
        
        # Check specific content
        poi_types = poims.get_poi_types()
        assert 'museum' in poi_types
        assert 'landmark' in poi_types
        
        # Verify POI loading
        pois = poims.get_pois()
        poi_names = [poi.get_name() for poi in pois]
        assert 'Louvre Abu Dhabi' in poi_names
        assert 'Sheikh Zayed Grand Mosque' in poi_names
    
    def test_initialization_nonexistent_config(self):
        """Test initialization with non-existent config file."""
        with patch('builtins.print') as mock_print:
            poims = PoiManagementSystem('nonexistent.yaml')
            mock_print.assert_called_with("Warning: 'nonexistent.yaml' file does not exist. Initializing from scratch.")
        
        assert len(poims.get_poi_types()) == 0
        assert len(poims.get_pois()) == 0
        assert len(poims.get_visitors()) == 0
    
    def test_initialization_empty_config(self):
        """Test initialization with empty config file."""
        # Create temporary empty config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
            yaml.dump({}, tmp_file)
            tmp_file_path = tmp_file.name
        
        try:
            with patch('builtins.print') as mock_print:
                poims = PoiManagementSystem(tmp_file_path)
                mock_print.assert_called_with("Warning: Config file is empty or invalid")
            
            assert len(poims.get_poi_types()) == 0
            assert len(poims.get_pois()) == 0
            assert len(poims.get_visitors()) == 0
        finally:
            os.unlink(tmp_file_path)


class TestPoiManagement:
    """Test POI-related operations."""
    
    @pytest.fixture
    def poims(self):
        """Create a PoiManagementSystem for testing."""
        return PoiManagementSystem()
    
    def test_add_poi_type(self, poims):
        """Test adding POI types."""
        success = poims.add_poi_type('restaurant', ['cuisine', 'price_range'])
        
        assert success is True
        poi_types = poims.get_poi_types()
        assert 'restaurant' in poi_types
        assert poi_types['restaurant']['attributes'] == ['cuisine', 'price_range']
        assert poi_types['restaurant']['num_pois'] == 0
    
    def test_add_poi_valid(self, poims):
        """Test adding valid POI."""
        poims.add_poi_type('museum', ['opening_hours'])
        success = poims.add_poi('Test Museum', 'museum', 100, 200, {'opening_hours': '9-5'})
        
        assert success is True
        assert len(poims.get_pois()) == 1
        
        poi = poims.get_pois()[0]
        assert poi.get_name() == 'Test Museum'
        assert poi.get_poi_type() == 'museum'
        assert poi.get_coordinates() == (100, 200)
    
    def test_add_poi_invalid_coordinates(self, poims):
        """Test adding POI with invalid coordinates."""
        # Test coordinates outside map bounds
        success1 = poims.add_poi('Invalid X', 'test', -10, 200)
        success2 = poims.add_poi('Invalid Y', 'test', 200, 1001)
        
        assert success1 is False
        assert success2 is False
        assert len(poims.get_pois()) == 0
    
    def test_delete_poi(self, poims):
        """Test deleting POI."""
        poims.add_poi('Test POI', 'test', 100, 200)
        assert len(poims.get_pois()) == 1
        
        success = poims.delete_poi('Test POI')
        assert success is True
        assert len(poims.get_pois()) == 0
    
    def test_delete_nonexistent_poi(self, poims):
        """Test deleting non-existent POI."""
        with patch('builtins.print') as mock_print:
            success = poims.delete_poi('Nonexistent POI')
            assert success is False
            mock_print.assert_called_with("Warning: Trying to delete non-existent POI: Nonexistent POI")
    
    def test_delete_poi_type(self, poims):
        """Test deleting POI type."""
        poims.add_poi_type('temporary', ['attr1'])
        success = poims.delete_poi_type('temporary')
        
        assert success is True
        assert 'temporary' not in poims.get_poi_types()
    
    def test_delete_poi_type_with_pois(self, poims):
        """Test deleting POI type that has POIs."""
        poims.add_poi_type('museum', ['hours'])
        poims.add_poi('Test Museum', 'museum', 100, 200)
        
        with patch('builtins.print') as mock_print:
            success = poims.delete_poi_type('museum')
            assert success is False
            mock_print.assert_called_with("Warning: museum has more than 0 POIs. Not deleting.")


class TestVisitorManagement:
    """Test visitor-related operations."""
    
    @pytest.fixture
    def poims_with_pois(self):
        """Create PoiManagementSystem with sample POIs."""
        poims = PoiManagementSystem()
        poims.add_poi('Museum A', 'museum', 100, 200)
        poims.add_poi('Park B', 'park', 300, 400)
        return poims
    
    def test_add_visitor_basic(self, poims_with_pois):
        """Test adding visitor without visits."""
        success = poims_with_pois.add_visitor('John Doe', 'American', [])
        
        assert success is True
        assert len(poims_with_pois.get_visitors()) == 1
        
        visitor = poims_with_pois.get_visitors()[0]
        assert visitor.get_name() == 'John Doe'
        assert visitor.get_nationality() == 'American'
        assert visitor.get_num_visits() == 0
    
    def test_add_visitor_with_valid_visits(self, poims_with_pois):
        """Test adding visitor with valid visits."""
        visits = [
            {'poi_name': 'Museum A', 'date': '15/09/2024', 'rating': 8},
            {'poi_name': 'Park B', 'date': '16/09/2024', 'rating': 7}
        ]
        success = poims_with_pois.add_visitor('Jane Smith', 'British', visits)
        
        assert success is True
        visitor = poims_with_pois.get_visitors()[0]
        assert visitor.get_num_visits() == 2
    
    def test_add_visitor_with_invalid_poi_reference(self, poims_with_pois):
        """Test adding visitor with visit to non-existent POI."""
        visits = [
            {'poi_name': 'Nonexistent POI', 'date': '15/09/2024', 'rating': 8}
        ]
        success = poims_with_pois.add_visitor('Test User', 'Unknown', visits)
        
        assert success is True
        visitor = poims_with_pois.get_visitors()[0]
        assert visitor.get_num_visits() == 0  # Invalid visit filtered out
    
    def test_delete_visitor(self, poims_with_pois):
        """Test deleting visitor."""
        poims_with_pois.add_visitor('Test Visitor', 'TestNation', [])
        assert len(poims_with_pois.get_visitors()) == 1
        
        success = poims_with_pois.delete_visitor('Test Visitor')
        assert success is True
        assert len(poims_with_pois.get_visitors()) == 0


class TestPoiQueries:
    """Test POI query methods."""
    
    @pytest.fixture
    def populated_poims(self):
        """Create PoiManagementSystem with sample data."""
        poims = PoiManagementSystem()
        
        # Add POI types
        poims.add_poi_type('museum', ['hours'])
        poims.add_poi_type('park', ['size'])
        
        # Add POIs
        poims.add_poi('Museum A', 'museum', 100, 100)
        poims.add_poi('Museum B', 'museum', 200, 200)
        poims.add_poi('Park A', 'park', 300, 300)
        poims.add_poi('Park B', 'park', 400, 400)
        
        return poims
    
    def test_get_pois_by_poi_type(self, populated_poims):
        """Test getting POIs by type."""
        museums = populated_poims.get_pois_by_poi_type('museum')
        parks = populated_poims.get_pois_by_poi_type('park')
        
        assert len(museums) == 2
        assert len(parks) == 2
        
        museum_names = [poi.get_name() for poi in museums]
        assert 'Museum A' in museum_names
        assert 'Museum B' in museum_names
    
    def test_get_nearest_pois(self, populated_poims):
        """Test getting nearest POI pair."""
        nearest_pair = populated_poims.get_nearest_pois()
        
        assert len(nearest_pair) == 2
        assert isinstance(nearest_pair[0], tuple)
        assert len(nearest_pair[0]) == 3  # (id, name, coordinates)
    
    def test_get_num_pois_per_poi_type(self, populated_poims):
        """Test getting POI count per type."""
        counts = populated_poims.get_num_pois_per_poi_type()
        
        assert counts['museum'] == 2
        assert counts['park'] == 2
    
    def test_get_pois_within_distance(self, populated_poims):
        """Test getting POIs within distance."""
        # Get POIs within 150 units of (100, 100)
        nearby_pois = populated_poims.get_pois_within_distance(100, 100, 150)
        
        assert len(nearby_pois) >= 1  # Should include at least Museum A at (100, 100)
        
        # Check return format: (poi_id, name, coordinates, type, distance)
        poi_data = nearby_pois[0]
        assert len(poi_data) == 5
    
    def test_get_pois_within_distance_invalid_coordinates(self, populated_poims):
        """Test POIs within distance with invalid coordinates."""
        with patch('builtins.print') as mock_print:
            result = populated_poims.get_pois_within_distance(-10, 2000, 100)
            assert result == []
            mock_print.assert_called_with("Warning: Coordinates (-10, 2000) outside map bounds (0-1000)")
    
    def test_get_k_closest_pois(self, populated_poims):
        """Test getting k closest POIs."""
        closest_pois = populated_poims.get_k_closest_pois(100, 100, 2)
        
        assert len(closest_pois) == 2
        
        # Check sorting (closest first)
        distances = [poi_data[4] for poi_data in closest_pois]
        assert distances[0] <= distances[1]
    
    def test_get_k_closest_pois_more_than_available(self, populated_poims):
        """Test requesting more POIs than available."""
        with patch('builtins.print') as mock_print:
            closest_pois = populated_poims.get_k_closest_pois(100, 100, 10)
            assert len(closest_pois) == 4  # Only 4 POIs in system
            mock_print.assert_called()  # Should print warning


class TestBoundaryCorrectness:
    """Test epsilon-based boundary detection."""
    
    @pytest.fixture
    def boundary_poims(self):
        """Create system with POIs for boundary testing."""
        poims = PoiManagementSystem()
        
        # Add POI at exact distance 5.0 from (0, 0) -> (3, 4)
        poims.add_poi('Exact Distance', 'test', 3, 4)
        
        # Add POI very close to distance 5.0 from (0, 0)
        poims.add_poi('Almost Exact', 'test', 3.0000001, 4)
        
        return poims
    
    def test_get_pois_in_boundary_exact(self, boundary_poims):
        """Test boundary detection with exact distance."""
        boundary_pois = boundary_poims.get_pois_in_boundary(0, 0, 5.0)
        
        assert len(boundary_pois) == 1
        assert boundary_pois[0][1] == 'Exact Distance'  # name field
    
    def test_get_pois_in_boundary_with_epsilon(self, boundary_poims):
        """Test boundary detection with epsilon tolerance."""
        # With larger epsilon, should find the almost-exact POI too
        boundary_pois = boundary_poims.get_pois_in_boundary(0, 0, 5.0, epsilon=1e-6)
        
        assert len(boundary_pois) == 2
    
    def test_get_pois_in_boundary_invalid_epsilon(self, boundary_poims):
        """Test boundary detection with invalid epsilon."""
        with patch('builtins.print') as mock_print:
            result = boundary_poims.get_pois_in_boundary(0, 0, 5.0, epsilon=-1)
            assert result == []
            mock_print.assert_called_with("Warning: Epsilon must be positive, got -1")


class TestVisitorPoiQueries:
    """Test visitor and POI relationship queries."""
    
    @pytest.fixture
    def visitor_poi_system(self):
        """Create system with visitors and POIs for testing."""
        poims = PoiManagementSystem()
        
        # Add POIs
        poims.add_poi('Museum A', 'museum', 100, 100)
        poims.add_poi('Museum B', 'museum', 200, 200)
        poims.add_poi('Park A', 'park', 300, 300)
        
        # Add visitors with visits
        visits1 = [
            {'poi_name': 'Museum A', 'date': '15/09/2024', 'rating': 8},
            {'poi_name': 'Park A', 'date': '16/09/2024', 'rating': 7}
        ]
        visits2 = [
            {'poi_name': 'Museum A', 'date': '17/09/2024', 'rating': 9}
        ]
        
        poims.add_visitor('Alice', 'American', visits1)
        poims.add_visitor('Bob', 'British', visits2)
        
        return poims
    
    def test_get_visited_pois(self, visitor_poi_system):
        """Test getting visited POIs for a visitor."""
        alice_visits = visitor_poi_system.get_visited_pois('Alice')
        
        assert len(alice_visits) == 2
        
        # Check return format: (poi_id, name, date)
        visit_data = alice_visits[0]
        assert len(visit_data) == 3
    
    def test_get_visited_pois_nonexistent_visitor(self, visitor_poi_system):
        """Test getting visits for non-existent visitor."""
        with patch('builtins.print') as mock_print:
            result = visitor_poi_system.get_visited_pois('Nonexistent')
            assert result == []
            mock_print.assert_called_with("`Nonexistent` not in Visitors")
    
    def test_get_num_visitors_per_poi(self, visitor_poi_system):
        """Test getting visitor count per POI."""
        visitor_counts = visitor_poi_system.get_num_visitors_per_poi()
        
        assert len(visitor_counts) == 3  # 3 POIs
        
        # Museum A should have 2 visitors (Alice and Bob)
        museum_a_count = next(count for poi_id, count in visitor_counts 
                             if any(poi.get_name() == 'Museum A' and poi.get_id() == poi_id 
                                   for poi in visitor_poi_system.get_pois()))
        assert museum_a_count == 2
    
    def test_get_num_pois_per_visitor(self, visitor_poi_system):
        """Test getting POI count per visitor."""
        poi_counts = visitor_poi_system.get_num_pois_per_visitor()
        
        assert len(poi_counts) == 2  # 2 visitors
        
        # Check format: (visitor_id, num_pois)
        alice_count = next(count for visitor_id, count in poi_counts 
                          if any(visitor.get_name() == 'Alice' and visitor.get_id() == visitor_id 
                                for visitor in visitor_poi_system.get_visitors()))
        assert alice_count == 2
    
    def test_get_crowdest_k_pois(self, visitor_poi_system):
        """Test getting most crowded POIs."""
        crowded_pois = visitor_poi_system.get_crowdest_k_pois(2)
        
        assert len(crowded_pois) <= 2
        # Check format: (poi_id, name)
        assert len(crowded_pois[0]) == 2
    
    def test_get_most_visited_k_visitors(self, visitor_poi_system):
        """Test getting most active visitors."""
        active_visitors = visitor_poi_system.get_most_visited_k_visitors(1)
        
        assert len(active_visitors) == 1
        # Alice should be the most active (2 visits vs Bob's 1)
        assert active_visitors[0][1] == 'Alice'  # name field
    
    def test_get_special_visitors(self, visitor_poi_system):
        """Test coverage fairness query."""
        # Alice visited 2 POIs across 2 types (museum, park)
        special_visitors = visitor_poi_system.get_special_visitors(m=2, t=2)
        
        assert len(special_visitors) == 1
        assert special_visitors[0][1] == 'Alice'  # name field
        assert special_visitors[0][3] == 2  # total POIs visited
        assert special_visitors[0][4] == 2  # distinct POI types


class TestRenameOperations:
    """Test rename operations (optional extensions)."""
    
    @pytest.fixture
    def rename_poims(self):
        """Create system for testing rename operations."""
        poims = PoiManagementSystem()
        poims.add_poi_type('museum', ['hours', 'fee'])
        poims.add_poi('Test Museum', 'museum', 100, 100, {'hours': '9-5', 'fee': '10'})
        return poims
    
    def test_rename_poi_type(self, rename_poims):
        """Test renaming POI type."""
        success = rename_poims.rename_poi_type('museum', 'art_gallery')
        
        assert success is True
        assert 'museum' not in rename_poims.get_poi_types()
        assert 'art_gallery' in rename_poims.get_poi_types()
        
        # Check that existing POI updated
        poi = rename_poims.get_pois()[0]
        assert poi.get_poi_type() == 'art_gallery'
    
    def test_rename_nonexistent_poi_type(self, rename_poims):
        """Test renaming non-existent POI type."""
        with patch('builtins.print') as mock_print:
            success = rename_poims.rename_poi_type('nonexistent', 'new_name')
            assert success is False
            mock_print.assert_called_with("Warning: `nonexistent` is non-existent in POI types")
    
    def test_rename_poi_type_attribute(self, rename_poims):
        """Test renaming POI type attribute."""
        success = rename_poims.rename_poi_type_attribute('museum', 'hours', 'opening_times')
        
        assert success is True
        poi_type = rename_poims.get_poi_types()['museum']
        assert 'hours' not in poi_type['attributes']
        assert 'opening_times' in poi_type['attributes']
        
        # Check that existing POI updated
        poi = rename_poims.get_pois()[0]
        attrs = poi.get_attributes()
        assert 'hours' not in attrs
        assert 'opening_times' in attrs
        assert attrs['opening_times'] == '9-5'


class TestSystemEquality:
    """Test system equality and representation."""
    
    def test_system_equality_empty(self):
        """Test equality of empty systems."""
        system1 = PoiManagementSystem()
        system2 = PoiManagementSystem()
        
        assert system1 == system2
    
    # TODO: fix the logic of not being equal if they get different IDs
    # def test_system_equality_with_data(self):
    #     """Test equality of systems with same data."""
    #     system1 = PoiManagementSystem()
    #     system1.add_poi_type('museum', ['hours'])
    #     system1.add_poi('Test Museum', 'museum', 100, 100)
        
    #     system2 = PoiManagementSystem()
    #     system2.add_poi_type('museum', ['hours'])
    #     system2.add_poi('Test Museum', 'museum', 100, 100)
        
    #     assert system1 == system2
    
    def test_system_inequality_different_data(self):
        """Test inequality of systems with different data."""
        system1 = PoiManagementSystem()
        system1.add_poi('POI A', 'test', 100, 100)
        
        system2 = PoiManagementSystem()
        system2.add_poi('POI B', 'test', 200, 200)
        
        assert system1 != system2
    
    def test_system_inequality_with_non_system(self):
        """Test inequality with non-system objects."""
        system = PoiManagementSystem()
        
        assert system != 'not a system'
        assert system != 123
        assert system != None
    
    def test_system_representation(self):
        """Test system string representation."""
        system = PoiManagementSystem()
        system.add_poi('Test POI', 'test', 100, 100)
        
        repr_str = repr(system)
        assert 'PoiManagementSystem' in repr_str
        assert 'Test POI' in repr_str


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_type_validation_errors(self):
        """Test that type validation errors are properly raised."""
        poims = PoiManagementSystem()
        
        with pytest.raises(ValueValidationError):
            poims.add_poi(123, 'test', 100, 100)  # poi_name should be string
        
        with pytest.raises(ValueValidationError):
            poims.get_pois_by_poi_type(['invalid'])  # poi_type should be string
    
    def test_empty_system_queries(self):
        """Test queries on empty system."""
        poims = PoiManagementSystem()
        
        assert poims.get_pois_by_poi_type('museum') == []
        assert poims.get_nearest_pois() == []
        assert poims.get_num_pois_per_poi_type() == {}
        assert poims.get_pois_within_distance(100, 100, 50) == []
        assert poims.get_k_closest_pois(100, 100, 5) == []
    
    def test_config_error_handling(self):
        """Test config file error handling."""
        # Create invalid YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp_file:
            tmp_file.write("invalid: yaml: content: [")  # Malformed YAML
            tmp_file_path = tmp_file.name
        
        try:
            with patch('builtins.print') as mock_print:
                poims = PoiManagementSystem(tmp_file_path)
                # Should handle YAML parsing error gracefully
                mock_print.assert_called()
        finally:
            os.unlink(tmp_file_path)
    
    def test_poi_deletion_updates_visitor_visits(self):
        """Test that deleting POI removes it from visitor visits."""
        poims = PoiManagementSystem()
        poims.add_poi('Test POI', 'test', 100, 100)
        poims.add_visitor('Test Visitor', 'TestNation', [
            {'poi_name': 'Test POI', 'date': '15/09/2024', 'rating': 8}
        ])
        
        # Verify visitor has the visit
        visitor = poims.get_visitors()[0]
        assert visitor.get_num_visits() == 1
        
        # Delete POI
        poims.delete_poi('Test POI')
        
        # Verify visit was removed from visitor
        visitor = poims.get_visitors()[0]
        assert visitor.get_num_visits() == 0
    
    def test_epsilon_default_value(self):
        """Test that epsilon uses class default when not specified."""
        poims = PoiManagementSystem()
        poims.add_poi('Test POI', 'test', 3, 4)  # Distance 5.0 from origin
        
        # Should use default epsilon
        boundary_pois_default = poims.get_pois_in_boundary(0, 0, 5.0)
        boundary_pois_explicit = poims.get_pois_in_boundary(0, 0, 5.0, epsilon=PoiManagementSystem.EPSILON)
        
        assert len(boundary_pois_default) == len(boundary_pois_explicit)