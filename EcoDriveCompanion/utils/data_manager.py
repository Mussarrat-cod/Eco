import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class DataManager:
    @staticmethod
    def get_driving_history():
        """Get driving history data."""
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        data = {
            'date': dates,
            'distance': np.random.normal(30, 10, 30),  # km
            'fuel_consumption': np.random.normal(6, 1, 30),  # L/100km
            'eco_score': np.random.normal(80, 10, 30),  # 0-100
            'harsh_braking': np.random.randint(0, 5, 30),
            'rapid_acceleration': np.random.randint(0, 5, 30)
        }
        return pd.DataFrame(data)

    @staticmethod
    def get_maintenance_schedule():
        """Get vehicle maintenance schedule."""
        current_date = datetime.now()
        maintenance_items = [
            {
                'item': 'Oil Change',
                'last_service': (current_date - timedelta(days=80)).strftime('%Y-%m-%d'),
                'next_due': (current_date + timedelta(days=10)).strftime('%Y-%m-%d'),
                'interval_km': 5000,
                'status': 'Due Soon'
            },
            {
                'item': 'Tire Rotation',
                'last_service': (current_date - timedelta(days=45)).strftime('%Y-%m-%d'),
                'next_due': (current_date + timedelta(days=45)).strftime('%Y-%m-%d'),
                'interval_km': 10000,
                'status': 'OK'
            },
            {
                'item': 'Air Filter',
                'last_service': (current_date - timedelta(days=150)).strftime('%Y-%m-%d'),
                'next_due': (current_date + timedelta(days=30)).strftime('%Y-%m-%d'),
                'interval_km': 15000,
                'status': 'Due Soon'
            }
        ]
        return pd.DataFrame(maintenance_items)

    @staticmethod
    def calculate_carbon_footprint(distance, fuel_consumption):
        """Calculate carbon footprint in kg CO2."""
        # Average CO2 emissions per liter of gasoline: 2.31 kg
        fuel_used = distance * fuel_consumption / 100  # L
        return fuel_used * 2.31

    @staticmethod
    def get_emissions_data():
        """Get historical emissions data."""
        dates = pd.date_range(end=datetime.now(), periods=12, freq='ME')
        data = {
            'date': dates,
            'emissions': np.random.normal(300, 50, 12),  # kg CO2
            'distance': np.random.normal(800, 100, 12),  # km
            'average_consumption': np.random.normal(7, 1, 12)  # L/100km
        }
        return pd.DataFrame(data)
