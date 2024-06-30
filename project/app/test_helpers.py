from app.helpers import get_coords_tuple, get_geocode_api_results
from project.settings import GMAPS_GEOCODE_API_URL
from typing import Tuple
import pytest
from unittest.mock import patch, MagicMock

def mock_get(url, params):
    mock_request = MagicMock()
    mock_response = {
        'results': [
            {
                'formatted_address': '1600 Amphitheatre Parkway, Mountain View, CA',
                'geometry': {
                    'location': {
                        'lat': 37.4224764,
                        'lng': -122.0842499
                    }
                }
            }
        ]
    }
    mock_request.json.return_value = mock_response
    return mock_request

@pytest.fixture
def mock_request_get(monkeypatch):
    monkeypatch.setattr('requests.get', mock_get)

def test_get_geocode_api_results(mock_request_get):
    expected_params = {
        'address': '1600 Amphitheatre Parkway, Mountain View, CA',
        'key': 'MOCK_API_KEY'
    }
    with patch('requests.get', side_effect=mock_get) as mock_get_func:
        result = get_geocode_api_results(expected_params)
        mock_get_func.assert_called_once_with(GMAPS_GEOCODE_API_URL, params=expected_params)
        assert result['formatted_address'] == '1600 Amphitheatre Parkway, Mountain View, CA'

@pytest.mark.parametrize("coords, expected, description", [
    ("1.23,4.56", (1.23, 4.56), "test positive coordinates"),
    ("-12.345,-67.89", (-12.345, -67.89), "test negative coordinates"),
    ("1,-2.5", (1.0, -2.5), "test passing an int"),
    ("90,180", (90, 180), "test maximum coordinates"),
    ("-90,-180", (-90, -180), "test minimum coordinates")
])
def test_get_coords_tuple(coords: str, expected: Tuple[float, float], description: str):
    assert get_coords_tuple(coords) == expected, description

@pytest.mark.parametrize("coords, description", [
    ("-90.01, 0", "test invalid latitude"),
    ("0, 181", "test invalid longitude"),
])
def test_get_coords_tuple_invalid_coords(coords: str, description: str):
    with pytest.raises(AssertionError):
        try:
            get_coords_tuple("invalid_format")
        except Exception as e:
            if isinstance(e, AssertionError):
                raise e
            assert False, description

