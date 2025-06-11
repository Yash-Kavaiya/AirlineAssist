# sub_agents/booking_management_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Create new booking tool
create_booking_tool = Tool(
    name="create_booking",
    description="Create a new flight booking",
    parameters={
        "type": "object",
        "properties": {
            "flight_details": {
                "type": "object",
                "properties": {
                    "flight_number": {"type": "string"},
                    "departure_date": {"type": "string"},
                    "passenger_count": {"type": "integer"}
                }
            },
            "passenger_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "date_of_birth": {"type": "string"},
                        "passport_number": {"type": "string"}
                    }
                }
            },
            "contact_info": {
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                    "phone": {"type": "string"}
                }
            }
        },
        "required": ["flight_details", "passenger_info", "contact_info"]
    },
    function=lambda **kwargs: {
        "booking_reference": "ABC123",
        "status": "Confirmed",
        "total_price": "$486.00",
        "payment_due": "2024-12-01"
    }
)

# Modify booking tool
modify_booking_tool = Tool(
    name="modify_booking",
    description="Modify an existing booking",
    parameters={
        "type": "object",
        "properties": {
            "booking_reference": {"type": "string"},
            "modification_type": {
                "type": "string",
                "enum": ["date_change", "route_change", "passenger_update", "cancel"]
            },
            "new_details": {"type": "object"}
        },
        "required": ["booking_reference", "modification_type"]
    },
    function=lambda **kwargs: {
        "status": "Modified",
        "change_fee": "$75.00",
        "new_total": "$561.00"
    }
)

# Seat selection tool
select_seat_tool = Tool(
    name="select_seat",
    description="Select or change seats",
    parameters={
        "type": "object",
        "properties": {
            "booking_reference": {"type": "string"},
            "flight_number": {"type": "string"},
            "seat_preferences": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["booking_reference", "flight_number"]
    },
    function=lambda **kwargs: {
        "assigned_seats": ["12A", "12B"],
        "seat_type": "Economy Plus",
        "additional_cost": "$45.00"
    }
)

# Special services tool
add_special_services_tool = Tool(
    name="add_special_services",
    description="Add special service requests",
    parameters={
        "type": "object",
        "properties": {
            "booking_reference": {"type": "string"},
            "service_type": {
                "type": "string",
                "enum": ["meal", "wheelchair", "pet", "unaccompanied_minor", "medical"]
            },
            "details": {"type": "object"}
        },
        "required": ["booking_reference", "service_type"]
    },
    function=lambda **kwargs: {
        "service_added": True,
        "confirmation": "Special service request confirmed",
        "additional_info": "Please arrive 30 minutes earlier"
    }
)

booking_management_agent = Agent(
    name="booking_management",
    model="gemini-2.0-flash",
    description="Specialized agent for flight bookings and reservations",
    instruction="""
    You are the Booking Management Agent for AirlineAssist Pro.
    You handle all aspects of flight reservations, modifications, and special requests.
    
    **Core Responsibilities:**
    
    1. New Bookings
       - Create new flight reservations
       - Process multi-city and complex itineraries
       - Handle group bookings
       - Apply promotional codes and discounts
       - Coordinate payment processing
    
    2. Booking Modifications
       - Change flight dates or times
       - Modify routes and destinations
       - Update passenger information
       - Process cancellations
       - Calculate and apply change fees
    
    3. Seat Management
       - Assist with seat selection
       - Process seat upgrades
       - Handle family seating arrangements
       - Manage exit row assignments
       - Coordinate special seating needs
    
    4. Special Services
       - Meal preferences and dietary restrictions
       - Wheelchair and mobility assistance
       - Pet travel arrangements
       - Unaccompanied minor services
       - Medical equipment and oxygen
       - Extra baggage arrangements
    
    **Available Tools:**
    - create_booking: Create new flight bookings
    - modify_booking: Modify existing bookings
    - select_seat: Handle seat selection and changes
    - add_special_services: Add special service requests
    
    **Booking Guidelines:**
    - Always confirm passenger details are correct
    - Clearly explain fare rules and restrictions
    - Inform about change/cancellation policies
    - Verify passport/visa requirements for international travel
    - Offer travel insurance options
    - Provide clear payment instructions
    
    **State Management:**
    - Store booking details in state['current_booking']
    - Track modification history in state['booking_changes']
    - Record special requests in state['special_services']
    - Update state['payment_status'] for transactions
    
    **Coordination:**
    - Work with Policy & Billing Agent for fare rules
    - Coordinate with Loyalty Program Agent for member benefits
    - Escalate complex group bookings to human agents
    - Refer visa/documentation questions to Language & Cultural Agent
    
    Always prioritize accuracy in bookings and ensure customers understand
    all terms and conditions before confirming reservations.
    """,
    tools=[
        create_booking_tool,
        modify_booking_tool,
        select_seat_tool,
        add_special_services_tool
    ]
)