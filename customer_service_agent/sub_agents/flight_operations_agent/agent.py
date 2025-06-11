# sub_agents/flight_operations_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Flight status checking tool
check_flight_status_tool = Tool(
    name="check_flight_status",
    description="Check real-time flight status",
    parameters={
        "type": "object",
        "properties": {
            "flight_number": {"type": "string", "description": "Flight number (e.g., AA123)"},
            "date": {"type": "string", "description": "Flight date (YYYY-MM-DD)"}
        },
        "required": ["flight_number", "date"]
    },
    function=lambda flight_number, date: {
        "status": "On Time",
        "departure": "14:30",
        "arrival": "17:45",
        "gate": "B12",
        "aircraft": "Boeing 737-800"
    }
)

# Flight search tool
search_flights_tool = Tool(
    name="search_flights",
    description="Search for available flights",
    parameters={
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "Origin airport code"},
            "destination": {"type": "string", "description": "Destination airport code"},
            "departure_date": {"type": "string", "description": "Departure date (YYYY-MM-DD)"},
            "return_date": {"type": "string", "description": "Return date for round trip (optional)"},
            "passengers": {"type": "integer", "description": "Number of passengers", "default": 1}
        },
        "required": ["origin", "destination", "departure_date"]
    },
    function=lambda **kwargs: {
        "flights": [
            {
                "flight_number": "AA123",
                "departure": "08:00",
                "arrival": "11:15",
                "price": "$245",
                "available_seats": 45
            },
            {
                "flight_number": "AA456",
                "departure": "14:30",
                "arrival": "17:45",
                "price": "$312",
                "available_seats": 23
            }
        ]
    }
)

# Weather information tool
check_weather_tool = Tool(
    name="check_weather",
    description="Check weather conditions at airports",
    parameters={
        "type": "object",
        "properties": {
            "airport_code": {"type": "string", "description": "Airport code (e.g., JFK)"}
        },
        "required": ["airport_code"]
    },
    function=lambda airport_code: {
        "conditions": "Clear",
        "temperature": "72°F",
        "visibility": "10 miles",
        "delays": "No weather delays"
    }
)

# Airport information tool
get_airport_info_tool = Tool(
    name="get_airport_info",
    description="Get airport services and information",
    parameters={
        "type": "object",
        "properties": {
            "airport_code": {"type": "string", "description": "Airport code (e.g., LAX)"}
        },
        "required": ["airport_code"]
    },
    function=lambda airport_code: {
        "terminals": 4,
        "lounges": ["Admirals Club", "Centurion Lounge"],
        "services": ["WiFi", "Currency Exchange", "Medical Center"],
        "parking": "Available - $25/day"
    }
)

flight_operations_agent = Agent(
    name="flight_operations",
    model="gemini-2.0-flash",
    description="Specialized agent for flight operations and real-time information",
    instruction="""
    You are the Flight Operations Agent for AirlineAssist Pro.
    Your expertise covers all aspects of flight operations, schedules, and real-time information.
    
    **Core Responsibilities:**
    
    1. Flight Status & Tracking
       - Provide real-time flight status updates
       - Track delays, cancellations, and schedule changes
       - Monitor gate changes and boarding information
       - Alert about connection risks
    
    2. Flight Search & Availability
       - Search for available flights based on customer criteria
       - Compare different flight options
       - Suggest alternative routes when needed
       - Check seat availability
    
    3. Weather & Disruption Management
       - Monitor weather conditions affecting flights
       - Provide updates on weather-related delays
       - Suggest alternatives during disruptions
       - Coordinate with Emergency Response Agent for severe situations
    
    4. Airport Services & Information
       - Provide airport layout and terminal information
       - Guide to lounges and amenities
       - Parking and ground transportation options
       - Security wait times and TSA PreCheck info
    
    **Available Tools:**
    - check_flight_status: Get real-time flight status
    - search_flights: Search for available flights
    - check_weather: Check airport weather conditions
    - get_airport_info: Get airport services information
    
    **Communication Guidelines:**
    - Always provide accurate, real-time information
    - Be proactive about potential issues (delays, tight connections)
    - Offer alternatives when flights are disrupted
    - Include relevant details (gates, terminals, boarding times)
    - Use 24-hour time format for clarity
    
    **State Management:**
    - Update state['flight_alerts'] for important changes
    - Track searched flights in state['flight_search_history']
    - Monitor connection risks in state['connection_risk']
    
    When detecting severe disruptions or emergencies, immediately flag for escalation
    to the Emergency Response Agent through the orchestrator.
    """,
    tools=[
        check_flight_status_tool,
        search_flights_tool,
        check_weather_tool,
        get_airport_info_tool
    ]
)