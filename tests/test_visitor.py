import pytest
from datetime import datetime
from yapoims.visitor import Visitor
from yapoims.utils import ValueValidationError


class TestVisitorInitialization:
    """Test visitor creation and initialization."""
    
    def test_visitor_creation_basic(self):
        """Test creating a visitor with basic information."""
        visitor = Visitor('V001', 'John Doe', 'American')
        
        assert visitor.get_id() == 'V001'
        assert visitor.get_name() == 'John Doe'
        assert visitor.get_nationality() == 'American'
        assert visitor.get_visits() == []
        assert visitor.get_num_visits() == 0
    
    def test_visitor_creation_with_valid_visits(self):
        """Test creating a visitor with valid visit data."""
        visits = [
            {'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8},
            {'poi_id': 'P002', 'date': '16/09/2024'},  # No rating
        ]
        visitor = Visitor('V001', 'Alice Smith', 'British', visits)
        
        assert visitor.get_num_visits() == 2
        assert len(visitor.get_visited_poi_ids()) == 2
        assert visitor.get_visits()[0]['rating'] == 8
        assert visitor.get_visits()[1]['rating'] is None
    
    def test_visitor_creation_filters_invalid_visits(self):
        """Test that invalid visits are filtered out during initialization."""
        visits = [
            {'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8},  # Valid
            {'poi_id': 'P002', 'date': '32/13/2024', 'rating': 5},  # Invalid date
            {'poi_id': 'P003', 'dates': '16/09/2024', 'rating': 7},  # Wrong field name
            {'poi_id': 'P004', 'date': '17/09/2024', 'rating': 15}, # Invalid rating
            'invalid_visit',  # Not a dict
        ]
        visitor = Visitor('V001', 'Test User', 'Unknown', visits)
        
        assert visitor.get_num_visits() == 2  # Only first and fourth (rating set to None)
        assert visitor.get_visits()[1]['rating'] is None  # Invalid rating becomes None


class TestVisitorQueries:
    """Test visitor query methods."""
    
    @pytest.fixture
    def sample_visitor(self):
        """Create a visitor with sample visit data for testing."""
        visits = [
            {'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8},
            {'poi_id': 'P002', 'date': '16/09/2024', 'rating': 6},
            {'poi_id': 'P001', 'date': '20/09/2024', 'rating': 9},  # Revisit P001
        ]
        return Visitor('V001', 'Test User', 'TestNation', visits)
    
    def test_get_visited_poi_ids_with_duplicates(self, sample_visitor):
        """Test getting visited POI IDs including duplicates."""
        poi_ids = sample_visitor.get_visited_poi_ids()
        assert poi_ids == ['P001', 'P002', 'P001']
        assert len(poi_ids) == 3
    
    def test_get_unique_visited_poi_ids(self, sample_visitor):
        """Test getting unique visited POI IDs."""
        unique_ids = sample_visitor.get_unique_visited_poi_ids()
        assert set(unique_ids) == {'P001', 'P002'}
        assert len(unique_ids) == 2
    
    def test_has_visited_poi(self, sample_visitor):
        """Test checking if visitor has visited specific POIs."""
        assert sample_visitor.has_visited_poi('P001') is True
        assert sample_visitor.has_visited_poi('P002') is True
        assert sample_visitor.has_visited_poi('P999') is False
    
    def test_get_visits_to_poi(self, sample_visitor):
        """Test getting all visits to a specific POI."""
        p001_visits = sample_visitor.get_visits_to_poi('P001')
        assert len(p001_visits) == 2
        assert p001_visits[0]['rating'] == 8
        assert p001_visits[1]['rating'] == 9
        
        p999_visits = sample_visitor.get_visits_to_poi('P999')
        assert len(p999_visits) == 0
    
    def test_get_average_rating(self, sample_visitor):
        """Test calculating average rating."""
        # Sample visitor has ratings: 8, 6, 9 -> average = 7.67
        avg = sample_visitor.get_average_rating()
        assert abs(avg - 7.666666666666667) < 1e-10
    
    def test_get_average_rating_no_ratings(self):
        """Test average rating when no visits have ratings."""
        visits = [
            {'poi_id': 'P001', 'date': '15/09/2024'},  # No rating
            {'poi_id': 'P002', 'date': '16/09/2024'},  # No rating
        ]
        visitor = Visitor('V001', 'No Ratings', 'TestNation', visits)
        assert visitor.get_average_rating() is None


class TestVisitManagement:
    """Test adding and managing visits."""
    
    def test_add_valid_visit(self):
        """Test adding a valid visit."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        success = visitor.add_visit('P001', '15/09/2024', 8)
        
        assert success is True
        assert visitor.get_num_visits() == 1
        assert visitor.get_visits()[0]['poi_id'] == 'P001'
        assert visitor.get_visits()[0]['rating'] == 8
    
    def test_add_visit_without_rating(self):
        """Test adding a visit without rating."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        success = visitor.add_visit('P001', '15/09/2024')
        
        assert success is True
        assert visitor.get_visits()[0]['rating'] is None
    
    def test_add_invalid_visit_bad_date(self):
        """Test adding visit with invalid date format."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        success = visitor.add_visit('P001', '2024-09-15', 8)  # Wrong format
        
        assert success is False
        assert visitor.get_num_visits() == 0
    
    def test_add_invalid_visit_bad_rating(self):
        """Test adding visit with invalid rating."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        success = visitor.add_visit('P001', '15/09/2024', 15)  # Rating > 10
        
        assert success is True  # Visit added but rating set to None
        assert visitor.get_visits()[0]['rating'] is None
    
    def test_delete_visit(self):
        """Test deleting a visit."""
        visits = [
            {'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8},
            {'poi_id': 'P002', 'date': '16/09/2024', 'rating': 6},
        ]
        visitor = Visitor('V001', 'Test User', 'TestNation', visits)
        
        success = visitor.delete_visit('P001')
        assert success is True
        assert visitor.get_num_visits() == 1
        assert not visitor.has_visited_poi('P001')
    
    def test_delete_nonexistent_visit(self):
        """Test deleting a visit that doesn't exist."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        success = visitor.delete_visit('P999')
        assert success is False


class TestDateValidation:
    """Test date validation edge cases."""
    
    @pytest.fixture
    def visitor(self):
        return Visitor('V001', 'Date Tester', 'TestNation')
    
    def test_valid_dates(self, visitor):
        """Test various valid date formats."""
        valid_dates = [
            '01/01/2024',  # Normal date
            '29/02/2024',  # Valid leap year
            '31/12/2023',  # End of year
        ]
        
        for date in valid_dates:
            success = visitor.add_visit(f'P{len(visitor.get_visits())}', date, 5)
            assert success is True, f"Date {date} should be valid"
    
    def test_invalid_dates(self, visitor):
        """Test various invalid date formats."""
        invalid_dates = [
            '32/01/2024',   # Invalid day
            '01/13/2024',   # Invalid month
            '29/02/2023',   # Invalid leap year
            '1/1/2024',     # Single digits
            '01/01/24',     # Two-digit year
            '2024-01-01',   # Wrong separator
            'invalid',      # Not a date
            '',             # Empty string
        ]
        
        initial_visits = visitor.get_num_visits()
        for date in invalid_dates:
            success = visitor.add_visit('P001', date, 5)
            assert success is False, f"Date {date} should be invalid"
        
        assert visitor.get_num_visits() == initial_visits


class TestVisitorImmutability:
    """Test that visitor core properties are immutable."""
    
    def test_cannot_modify_id(self):
        """Test that visitor ID cannot be modified."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'id'"):
            visitor.id = 'V002'
    
    def test_cannot_modify_name(self):
        """Test that visitor name cannot be modified."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'name'"):
            visitor.name = 'New Name'
    
    def test_cannot_modify_nationality(self):
        """Test that visitor nationality cannot be modified."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        with pytest.raises(AttributeError, match="Cannot set attribute 'nationality'"):
            visitor.nationality = 'NewNation'
    
    def test_cannot_delete_attributes(self):
        """Test that visitor attributes cannot be deleted."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        with pytest.raises(AttributeError, match="Cannot delete attribute 'id'"):
            del visitor.id


class TestVisitorEquality:
    """Test visitor equality comparison."""
    
    def test_visitor_equality_identical(self):
        """Test that identical visitors are equal."""
        visits = [{'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8}]
        visitor1 = Visitor('V001', 'Test User', 'TestNation', visits)
        visitor2 = Visitor('V001', 'Test User', 'TestNation', visits)
        
        assert visitor1 == visitor2
        assert visitor1 == visitor1  # Self-equality
    
    def test_visitor_equality_different_ids(self):
        """Test that visitors with different IDs are not equal."""
        visitor1 = Visitor('V001', 'Test User', 'TestNation')
        visitor2 = Visitor('V002', 'Test User', 'TestNation')
        
        assert visitor1 != visitor2
    
    def test_visitor_equality_different_visits(self):
        """Test that visitors with different visits are not equal."""
        visitor1 = Visitor('V001', 'Test User', 'TestNation', 
                          [{'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8}])
        visitor2 = Visitor('V001', 'Test User', 'TestNation', 
                          [{'poi_id': 'P002', 'date': '15/09/2024', 'rating': 8}])
        
        assert visitor1 != visitor2
    
    def test_visitor_equality_with_non_visitor(self):
        """Test that visitor is not equal to non-visitor objects."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        assert visitor != 'not a visitor'
        assert visitor != 123
        assert visitor != None
        assert visitor != {}


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_type_validation_error(self):
        """Test that type validation errors are properly raised."""
        visitor = Visitor('V001', 'Test User', 'TestNation')
        
        with pytest.raises(ValueValidationError):
            visitor.delete_visit(123)  # poi_id should be string
    
    def test_visitor_representation(self):
        """Test visitor string representation."""
        visits = [{'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8}]
        visitor = Visitor('V001', 'Test User', 'TestNation', visits)
        
        repr_str = repr(visitor)
        assert 'V001' in repr_str
        assert 'Test User' in repr_str
        assert 'TestNation' in repr_str
        assert 'P001' in repr_str
    
    def test_empty_visits_list(self):
        """Test visitor with explicitly empty visits list."""
        visitor = Visitor('V001', 'Test User', 'TestNation', [])
        
        assert visitor.get_num_visits() == 0
        assert visitor.get_visits() == []
        assert visitor.get_visited_poi_ids() == []
        assert visitor.get_unique_visited_poi_ids() == []
    
    def test_visits_list_immutability(self):
        """Test that returned visits list doesn't affect internal state."""
        visits = [{'poi_id': 'P001', 'date': '15/09/2024', 'rating': 8}]
        visitor = Visitor('V001', 'Test User', 'TestNation', visits)
        
        # Modify returned list
        returned_visits = visitor.get_visits()
        returned_visits.append({'poi_id': 'P999', 'date': '01/01/2024'})
        
        # Internal state should be unchanged
        assert visitor.get_num_visits() == 1
        assert len(visitor.get_visits()) == 1