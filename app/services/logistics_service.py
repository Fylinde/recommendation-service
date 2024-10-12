from typing import List, Dict

# Placeholder warehouse data
WAREHOUSES = [
    {"id": 1, "location": "New York", "capacity": 100, "available_space": 50},
    {"id": 2, "location": "Los Angeles", "capacity": 120, "available_space": 40},
    {"id": 3, "location": "Chicago", "capacity": 80, "available_space": 70},
]

def get_warehouse_info() -> List[Dict]:
    """
    Simulates fetching warehouse data from the logistics service.
    This data can include warehouse ID, location, capacity, and available space.
    
    :return: A list of dictionaries containing warehouse information.
    """
    return WAREHOUSES

def find_nearest_warehouse_for_region(region: str, warehouse_data: List[Dict]) -> Dict:
    """
    Finds the nearest warehouse to the given region.
    Placeholder logic: Just returns the first warehouse in the list.
    
    In a real system, this would use geolocation or other logic to determine proximity.
    
    :param region: The region to find the nearest warehouse for.
    :param warehouse_data: A list of warehouse information to select from.
    :return: A dictionary representing the nearest warehouse.
    """
    # Placeholder logic: Returning the first available warehouse for demonstration
    return warehouse_data[0] if warehouse_data else {}
