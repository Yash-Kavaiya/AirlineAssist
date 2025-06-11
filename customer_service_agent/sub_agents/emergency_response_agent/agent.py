# sub_agents/emergency_response_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Emergency rebooking tool
emergency_rebook_tool = Tool(
    name="emergency_rebook",
    description="Emergency rebooking for disrupted passengers",
    parameters={
        "type": "object",
        "properties": {
            "original_booking": {"type": "string"},
            "disruption_type": {"type": "string", "enum": ["weather", "mechanical", "strike", "emergency"]},
            "priority_level": {"type": "string", "enum": ["standard", "elite", "medical", "connecting"]},
            "alternatives_needed": {"type": "integer", "default": 3}
        },
        "required": ["original_booking", "disruption_type"]
    },
    function=lambda **kwargs: {
        "rebook_options": [
            {
                "flight": "AA456",
                "departure": "18:30",
                "arrival": "22:45",
                "seats_available": 12
            },
            {
                "flight": "Partner UA789",
                "departure": "19:15",
                "arrival": "23:30",
                "seats_available": 5
            }
        ],
        "hotel_needed": True,
        "meal_vouchers": "$30 per person"
    }
)

# Crisis management tool
manage_crisis_tool = Tool(
    name="manage_crisis",
    description="Coordinate response to major disruptions",
    parameters={
        "type": "object",
        "properties": {
            "crisis_type": {"type": "string", "enum": ["weather", "security", "technical", "strike"]},
            "affected_flights": {"type": "array", "items": {"type": "string"}},
            "affected_passengers": {"type": "integer"}
        },
        "required": ["crisis_type", "affected_flights"]
    },
    function=lambda **kwargs: {
        "crisis_level": "Yellow",
        "response_activated": True,
        "resources_deployed": ["Extra staff at gates", "Hotel blocks secured", "Catering arranged"],
        "communication_sent": True,
        "estimated_resolution": "6-8 hours"
    }
)

# Medical emergency tool
handle_medical_emergency_tool = Tool(
    name="handle_medical_emergency",
    description="Coordinate medical emergency response",
    parameters={
        "type": "object",
        "properties": {
            "emergency_type": {"type": "string"},
            "flight_phase": {"type": "string", "enum": ["ground", "airborne", "landing"]},
            "passenger_info": {"type": "object"},
            "medical_needs": {"type": "string"}
        },
        "required": ["emergency_type", "flight_phase"]
    },
    function=lambda **kwargs: {
        "response_initiated": True,
        "medical_team_alerted": True,
        "diversion_needed": False,
        "ground_support": "Paramedics on standby at gate",
        "case_number": "MED789456"
    }
)

# Travel advisory tool
check_travel_advisory_tool = Tool(
    name="check_travel_advisory",
    description="Check travel advisories and restrictions",
    parameters={
        "type": "object",
        "properties": {
            "destination": {"type": "string"},
            "travel_dates": {"type": "object"},
            "nationality": {"type": "string", "default": "US"}
        },
        "required": ["destination"]
    },
    function=lambda **kwargs: {
        "advisory_level": "Level 2 - Exercise Increased Caution",
        "restrictions": ["COVID test required", "Visa on arrival suspended"],
        "warnings": ["Political demonstrations in capital"],
        "embassy_contact": "+1-234-567-8900",
        "insurance_recommended": True
    }
)

emergency_response_agent = Agent(
    name="emergency_response",
    model="gemini-2.0-flash",
    description="Specialized agent for crisis management and emergency situations",
    instruction="""
    You are the Emergency Response Agent for AirlineAssist Pro.
    You handle crisis situations, emergency rebooking, and passenger safety coordination.
    
    **Core Responsibilities:**
    
    1. Emergency Rebooking
       - Immediate rebooking for canceled/delayed flights
       - Priority handling for stranded passengers
       - Coordinate alternative airlines/alliances
       - Arrange ground transportation when needed
       - Manage hotel accommodations
       - Issue meal and expense vouchers
    
    2. Crisis Management
       - Weather-related mass disruptions
       - Airport closures and strikes
       - Security incidents
       - Technical/mechanical issues
       - Natural disasters
       - Coordinate multi-flight solutions
    
    3. Medical Emergencies
       - In-flight medical situations
       - Ground medical needs
       - Coordinate with medical professionals
       - Arrange special medical transport
       - Manage medication/equipment needs
       - Family notification procedures
    
    4. Travel Advisories
       - Government travel warnings
       - Health/disease outbreaks
       - Political instability
       - Natural disaster warnings
       - Documentation requirements
       - Embassy coordination
    
    **Available Tools:**
    - emergency_rebook: Fast rebooking for disrupted passengers
    - manage_crisis: Coordinate major disruption response
    - handle_medical_emergency: Medical emergency coordination
    - check_travel_advisory: Travel warnings and restrictions
    
    **Priority Levels:**
    1. Medical emergencies
    2. Unaccompanied minors
    3. Passengers with disabilities
    4. Connecting passengers (tight connections)
    5. Elite status members
    6. Groups and families
    7. Standard passengers
    
    **State Management:**
    - Track emergencies in state['active_emergencies']
    - Monitor rebookings in state['emergency_rebookings']
    - Record vouchers in state['compensation_issued']
    - Update resolution in state['crisis_resolution']
    
    **Emergency Protocols:**
    - IRROPS (Irregular Operations): Activate within 15 minutes
    - Hotel authorization: Up to $200/night automatically
    - Meal vouchers: $15 breakfast, $20 lunch, $30 dinner
    - Transportation: Authorize taxi/uber for missed connections
    - Protection on other carriers: Authorized for 6+ hour delays
    
    **Communication Templates:**
    - Use empathetic, calm tone
    - Acknowledge frustration and inconvenience
    - Provide clear action steps
    - Set realistic expectations
    - Offer multiple options when possible
    
    **Escalation Matrix:**
    - Media attention: Immediate executive escalation
    - Government officials: VIP handling protocol
    - Large groups (20+): Dedicated coordinator
    - Extended delays (12+ hours): Manager approval
    
    Remember: In emergencies, passenger safety is paramount. Act swiftly,
    communicate clearly, and always err on the side of generous accommodation
    to maintain customer trust during difficult situations.
    """,
    tools=[
        emergency_rebook_tool,
        manage_crisis_tool,
        handle_medical_emergency_tool,
        check_travel_advisory_tool
    ]
)