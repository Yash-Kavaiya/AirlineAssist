# sub_agents/baggage_services_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Track baggage tool
track_baggage_tool = Tool(
    name="track_baggage",
    description="Track baggage location and status",
    parameters={
        "type": "object",
        "properties": {
            "reference_number": {"type": "string", "description": "Baggage tag or reference number"},
            "last_name": {"type": "string", "description": "Passenger last name"}
        },
        "required": ["reference_number", "last_name"]
    },
    function=lambda **kwargs: {
        "status": "In Transit",
        "last_scan": "JFK Airport - 14:30",
        "expected_arrival": "LAX Airport - 18:45",
        "current_location": "En route on AA123"
    }
)

# File baggage claim tool
file_baggage_claim_tool = Tool(
    name="file_baggage_claim",
    description="File a claim for lost or damaged baggage",
    parameters={
        "type": "object",
        "properties": {
            "claim_type": {"type": "string", "enum": ["lost", "damaged", "delayed"]},
            "booking_reference": {"type": "string"},
            "baggage_description": {
                "type": "object",
                "properties": {
                    "color": {"type": "string"},
                    "brand": {"type": "string"},
                    "size": {"type": "string"},
                    "identifying_features": {"type": "string"}
                }
            },
            "contents_value": {"type": "number"}
        },
        "required": ["claim_type", "booking_reference", "baggage_description"]
    },
    function=lambda **kwargs: {
        "claim_number": "CLM789456",
        "status": "Filed",
        "estimated_resolution": "3-5 business days",
        "compensation_eligible": True
    }
)

# Check baggage policy tool
check_baggage_policy_tool = Tool(
    name="check_baggage_policy",
    description="Check baggage allowances and fees",
    parameters={
        "type": "object",
        "properties": {
            "route_type": {"type": "string", "enum": ["domestic", "international"]},
            "fare_class": {"type": "string", "enum": ["economy", "premium_economy", "business", "first"]},
            "loyalty_status": {"type": "string", "default": "none"}
        },
        "required": ["route_type", "fare_class"]
    },
    function=lambda **kwargs: {
        "free_allowance": {
            "carry_on": "1 bag + 1 personal item",
            "checked": "1 bag up to 50 lbs"
        },
        "excess_fees": {
            "second_bag": "$40",
            "third_bag": "$150",
            "overweight": "$100 (51-70 lbs)"
        },
        "restricted_items": ["Lithium batteries", "Flammable liquids"]
    }
)

# Arrange special baggage tool
arrange_special_baggage_tool = Tool(
    name="arrange_special_baggage",
    description="Arrange handling for special baggage items",
    parameters={
        "type": "object",
        "properties": {
            "booking_reference": {"type": "string"},
            "item_type": {
                "type": "string",
                "enum": ["sports_equipment", "musical_instrument", "fragile", "oversized", "medical"]
            },
            "item_details": {"type": "object"}
        },
        "required": ["booking_reference", "item_type"]
    },
    function=lambda **kwargs: {
        "arrangement_confirmed": True,
        "special_handling_fee": "$75",
        "check_in_instructions": "Please arrive 60 minutes early for special handling"
    }
)

baggage_services_agent = Agent(
    name="baggage_services",
    model="gemini-2.0-flash",
    description="Specialized agent for baggage tracking, claims, and policies",
    instruction="""
    You are the Baggage Services Agent for AirlineAssist Pro.
    You handle all baggage-related inquiries, tracking, claims, and special arrangements.
    
    **Core Responsibilities:**
    
    1. Baggage Tracking
       - Real-time baggage location tracking
       - Provide status updates on delayed bags
       - Estimate delivery times for delayed baggage
       - Coordinate baggage transfers for connections
       - Track priority and rush tags
    
    2. Lost & Damaged Claims
       - File claims for lost baggage
       - Process damaged baggage reports
       - Calculate compensation amounts
       - Provide claim status updates
       - Coordinate temporary expense reimbursements
       - Arrange baggage delivery once found
    
    3. Baggage Policies
       - Explain size and weight limits
       - Calculate excess baggage fees
       - Clarify restricted and prohibited items
       - Advise on international baggage rules
       - Apply loyalty program benefits
    
    4. Special Baggage Handling
       - Sports equipment (golf, ski, surf, bikes)
       - Musical instruments
       - Fragile and valuable items
       - Medical equipment
       - Oversized items
       - Pet carriers
    
    **Available Tools:**
    - track_baggage: Track baggage location and status
    - file_baggage_claim: File claims for lost/damaged baggage
    - check_baggage_policy: Check allowances and fees
    - arrange_special_baggage: Arrange special item handling
    
    **Service Guidelines:**
    - Show empathy for baggage issues
    - Provide realistic timeframes for resolution
    - Clearly explain compensation policies
    - Offer interim solutions (emergency kit, expense coverage)
    - Document all details thoroughly
    
    **State Management:**
    - Track active claims in state['baggage_claims']
    - Monitor delayed bags in state['delayed_baggage']
    - Record special handling in state['special_baggage']
    - Update delivery status in state['baggage_delivery']
    
    **Compensation Guidelines:**
    - Delayed baggage: Up to $50/day for essentials (max 5 days)
    - Lost baggage: Up to $3,800 for domestic, Montreal Convention for international
    - Damaged items: Actual value with depreciation
    - Always verify receipts for reimbursement
    
    **Escalation Triggers:**
    - High-value claims (over $1,000)
    - Diplomatic or military baggage
    - Medical equipment issues
    - Repeated claim history
    
    Always maintain detailed records and provide claim reference numbers.
    Be proactive in offering solutions and keeping customers informed of progress.
    """,
    tools=[
        track_baggage_tool,
        file_baggage_claim_tool,
        check_baggage_policy_tool,
        arrange_special_baggage_tool
    ]
)