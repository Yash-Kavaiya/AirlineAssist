# sub_agents/loyalty_program_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Check miles balance tool
check_miles_balance_tool = Tool(
    name="check_miles_balance",
    description="Check frequent flyer miles balance and activity",
    parameters={
        "type": "object",
        "properties": {
            "member_number": {"type": "string"},
            "include_activity": {"type": "boolean", "default": True}
        },
        "required": ["member_number"]
    },
    function=lambda **kwargs: {
        "current_balance": 75420,
        "lifetime_miles": 524300,
        "qualifying_miles": 42000,
        "recent_activity": [
            {"date": "2024-11-15", "description": "Flight AA123", "miles": 2340},
            {"date": "2024-11-01", "description": "Partner purchase", "miles": 450}
        ],
        "expiring_soon": {"miles": 5000, "expiry_date": "2025-03-31"}
    }
)

# Redeem miles tool
redeem_miles_tool = Tool(
    name="redeem_miles",
    description="Redeem miles for flights or upgrades",
    parameters={
        "type": "object",
        "properties": {
            "member_number": {"type": "string"},
            "redemption_type": {"type": "string", "enum": ["flight", "upgrade", "hotel", "car"]},
            "details": {"type": "object"}
        },
        "required": ["member_number", "redemption_type", "details"]
    },
    function=lambda **kwargs: {
        "redemption_confirmed": True,
        "miles_used": 25000,
        "confirmation_code": "RWRD789",
        "remaining_balance": 50420,
        "value_received": "$450"
    }
)

# Check status benefits tool
check_status_benefits_tool = Tool(
    name="check_status_benefits",
    description="Check member status and benefits",
    parameters={
        "type": "object",
        "properties": {
            "member_number": {"type": "string"}
        },
        "required": ["member_number"]
    },
    function=lambda **kwargs: {
        "current_status": "Gold",
        "benefits": [
            "Priority check-in",
            "2 free checked bags",
            "Priority boarding",
            "25% bonus miles",
            "Lounge access (with guest)"
        ],
        "qualifying_progress": {
            "miles_to_next": 8000,
            "segments_to_next": 10,
            "next_status": "Platinum"
        }
    }
)

# Transfer miles tool
transfer_miles_tool = Tool(
    name="transfer_miles",
    description="Transfer miles between accounts or partners",
    parameters={
        "type": "object",
        "properties": {
            "from_account": {"type": "string"},
            "to_account": {"type": "string"},
            "miles_amount": {"type": "integer"},
            "transfer_type": {"type": "string", "enum": ["member", "partner", "family"]}
        },
        "required": ["from_account", "to_account", "miles_amount"]
    },
    function=lambda **kwargs: {
        "transfer_completed": True,
        "miles_transferred": 10000,
        "transfer_fee": "$75",
        "new_balance": 65420,
        "transaction_id": "TRF456789"
    }
)

loyalty_program_agent = Agent(
    name="loyalty_program",
    model="gemini-2.0-flash",
    description="Specialized agent for frequent flyer program management",
    instruction="""
    You are the Loyalty Program Agent for AirlineAssist Pro.
    You manage all aspects of the frequent flyer program and member benefits.
    
    **Core Responsibilities:**
    
    1. Account Management
       - Check miles/points balance
       - Review account activity and statements
       - Update member information
       - Merge duplicate accounts
       - Recover missing miles
       - Handle account security
    
    2. Miles Redemption
       - Award flight bookings
       - Upgrade redemptions
       - Partner redemptions (hotels, cars, merchandise)
       - Miles + cash options
       - Award availability search
       - Waitlist management
    
    3. Status & Benefits
       - Explain tier benefits
       - Track qualification progress
       - Process status matches
       - Apply status benefits to bookings
       - Lounge access verification
       - Companion certificates
    
    4. Partner Programs
       - Transfer miles to/from partners
       - Earn miles with partners
       - Alliance benefits
       - Credit card mileage programs
       - Shopping and dining portals
    
    **Available Tools:**
    - check_miles_balance: Check miles balance and activity
    - redeem_miles: Process miles redemption
    - check_status_benefits: Check status level and benefits
    - transfer_miles: Transfer miles between accounts
    
    **Service Guidelines:**
    - Protect member account security
    - Maximize value for member redemptions
    - Clearly explain earning and redemption rates
    - Proactively mention expiring miles
    - Suggest ways to maintain/achieve status
    
    **State Management:**
    - Track member info in state['loyalty_member']
    - Monitor redemptions in state['redemption_history']
    - Record missing miles in state['mileage_claims']
    - Update tier progress in state['status_progress']
    
    **Redemption Values:**
    - Domestic economy: 12,500 miles one-way
    - Domestic business: 25,000 miles one-way
    - International economy: 30,000+ miles one-way
    - International business: 57,500+ miles one-way
    - Upgrades: Starting at 15,000 miles + copay
    
    **Elite Status Tiers:**
    - Silver: 25,000 miles OR 30 segments
    - Gold: 50,000 miles OR 60 segments
    - Platinum: 75,000 miles OR 90 segments
    - Diamond: 125,000 miles OR 120 segments
    
    **Special Situations:**
    - Status match: Requires proof from competitor
    - Mileage claims: Up to 12 months retroactive
    - Account merge: Requires identity verification
    - Deceased member: Transfer to beneficiary allowed
    
    Always emphasize the value of loyalty membership and help members
    maximize their benefits. Be knowledgeable about partner opportunities
    and creative redemption options.
    """,
    tools=[
        check_miles_balance_tool,
        redeem_miles_tool,
        check_status_benefits_tool,
        transfer_miles_tool
    ]
)