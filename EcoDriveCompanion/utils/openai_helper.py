import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_driving_tips(driving_data):
    """Generate eco-driving tips based on driving behavior."""
    try:
        # Process the driving data into a more readable format
        processed_data = {
            "eco_score": [float(score) for score in driving_data.get('eco_score', {}).values()],
            "fuel_consumption": [float(consumption) for consumption in driving_data.get('fuel_consumption', {}).values()],
            "harsh_braking": [int(events) for events in driving_data.get('harsh_braking', {}).values()],
            "rapid_acceleration": [int(events) for events in driving_data.get('rapid_acceleration', {}).values()],
        }
        
        # Calculate averages for a cleaner prompt
        avg_eco_score = sum(processed_data["eco_score"]) / len(processed_data["eco_score"]) if processed_data["eco_score"] else 0
        avg_fuel_consumption = sum(processed_data["fuel_consumption"]) / len(processed_data["fuel_consumption"]) if processed_data["fuel_consumption"] else 0
        total_harsh_braking = sum(processed_data["harsh_braking"])
        total_rapid_acceleration = sum(processed_data["rapid_acceleration"])
        
        # Create a summarized version of the data
        data_summary = {
            "average_eco_score": round(avg_eco_score, 2),
            "average_fuel_consumption": round(avg_fuel_consumption, 2),
            "total_harsh_braking_events": total_harsh_braking,
            "total_rapid_acceleration_events": total_rapid_acceleration
        }
        
        # Create the prompt with the summarized data
        prompt = f"""
        Based on the following driving data from the past week:
        - Average Eco Score: {data_summary['average_eco_score']} (scale 0-100, higher is better)
        - Average Fuel Consumption: {data_summary['average_fuel_consumption']} L/100km
        - Total Harsh Braking Events: {data_summary['total_harsh_braking_events']}
        - Total Rapid Acceleration Events: {data_summary['total_rapid_acceleration_events']}
        
        Please provide 3 specific eco-driving tips that will help improve fuel efficiency and reduce emissions.
        """
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an eco-driving expert. Analyze the driving data and provide specific, actionable tips for improvement. Format your response as a JSON object with a 'tips' array containing 3 specific tips."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
    except Exception as e:
        # Return a default JSON response in case of an error
        default_response = {
            "tips": [
                "Practice gradual acceleration to improve fuel efficiency.",
                "Maintain a steady speed and avoid unnecessary braking.",
                "Regular vehicle maintenance keeps your car running efficiently."
            ]
        }
        return json.dumps(default_response)

def analyze_maintenance_needs(vehicle_data):
    """Analyze vehicle data and suggest maintenance actions."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a vehicle maintenance expert. Analyze the vehicle data and suggest maintenance actions."
                },
                {
                    "role": "user",
                    "content": f"Based on this vehicle data, what maintenance is needed: {vehicle_data}"
                }
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        # Return a default JSON response in case of an error
        default_response = {
            "maintenance_actions": [
                "Check tire pressure and inflate to recommended levels.",
                "Consider scheduling an oil change in the next 30 days.",
                "Inspect air filters and replace if dirty."
            ]
        }
        return json.dumps(default_response)
