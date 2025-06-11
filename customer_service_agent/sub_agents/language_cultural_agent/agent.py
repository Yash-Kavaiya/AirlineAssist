# sub_agents/language_cultural_agent/agent.py
from google.adk.agents import Agent
from google.adk.tools import Tool

# Translation tool
translate_content_tool = Tool(
    name="translate_content",
    description="Translate content between languages",
    parameters={
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "source_language": {"type": "string", "default": "auto"},
            "target_language": {"type": "string"}
        },
        "required": ["text", "target_language"]
    },
    function=lambda **kwargs: {
        "translated_text": "Translated content here",
        "detected_language": "English",
        "confidence": 0.98
    }
)

# Visa requirements tool
check_visa_requirements_tool = Tool(
    name="check_visa_requirements",
    description="Check visa and documentation requirements",
    parameters={
        "type": "object",
        "properties": {
            "nationality": {"type": "string"},
            "destination": {"type": "string"},
            "purpose": {"type": "string", "enum": ["tourism", "business", "transit", "student"]},
            "duration": {"type": "integer", "description": "Stay duration in days"}
        },
        "required": ["nationality", "destination", "purpose"]
    },
    function=lambda **kwargs: {
        "visa_required": True,
        "visa_type": "Tourist visa",
        "processing_time": "5-7 business days",
        "requirements": [
            "Valid passport (6 months validity)",
            "Completed application form",
            "2 passport photos",
            "Proof of accommodation",
            "Return ticket"
        ],
        "fee": "$160",
        "visa_on_arrival": False
    }
)

# Cultural guidance tool
provide_cultural_guidance_tool = Tool(
    name="provide_cultural_guidance",
    description="Provide cultural information and etiquette",
    parameters={
        "type": "object",
        "properties": {
            "destination": {"type": "string"},
            "topics": {
                "type": "array",
                "items": {"type": "string", "enum": ["customs", "etiquette", "dress_code", "tipping", "language"]}
            }
        },
        "required": ["destination"]
    },
    function=lambda **kwargs: {
        "cultural_tips": {
            "greetings": "Bow slightly when meeting",
            "dress_code": "Conservative, remove shoes indoors",
            "tipping": "Not customary, may be refused",
            "customs": "Gift giving is important",
            "taboos": "Don't point with feet"
        },
        "useful_phrases": {
            "hello": "Konnichiwa",
            "thank_you": "Arigato",
            "excuse_me": "Sumimasen"
        }
    }
)

# Time zone tool
calculate_time_zones_tool = Tool(
    name="calculate_time_zones",
    description="Calculate time differences and optimal contact times",
    parameters={
        "type": "object",
        "properties": {
            "origin_timezone": {"type": "string"},
            "destination_timezone": {"type": "string"},
            "preferred_time": {"type": "string", "description": "Time in origin timezone"}
        },
        "required": ["origin_timezone", "destination_timezone"]
    },
    function=lambda **kwargs: {
        "time_difference": "+13 hours",
        "current_time_origin": "10:00 AM EST",
        "current_time_destination": "11:00 PM JST (next day)",
        "business_hours_overlap": "8:00 PM - 10:00 PM EST",
        "jet_lag_advice": "Expect 5-7 days adjustment"
    }
)

language_cultural_agent = Agent(
    name="language_cultural",
    model="gemini-2.0-flash",
    description="Specialized agent for language support and cultural guidance",
    instruction="""
    You are the Language & Cultural Agent for AirlineAssist Pro.
    You provide multilingual support, cultural guidance, and international travel assistance.
    
    **Core Responsibilities:**
    
    1. Language Support
       - Real-time translation services
       - Multilingual customer assistance
       - Document translation
       - Interpretation of announcements
       - Language-specific booking help
       - Emergency translation services
    
    2. Visa & Documentation
       - Visa requirement verification
       - Passport validity checking
       - Entry/exit requirements
       - Health documentation (vaccines, tests)
       - Customs declarations assistance
       - Travel authorization (ESTA, eTA, etc.)
    
    3. Cultural Guidance
       - Business etiquette by country
       - Social customs and norms
       - Religious considerations
       - Dress code recommendations
       - Gift-giving protocols
       - Dining etiquette
       - Tipping guidelines
    
    4. International Travel Support
       - Time zone calculations
       - Currency information
       - Local transportation guidance
       - Embassy/consulate contacts
       - Emergency phrases
       - Local law awareness
       - Health and safety tips
    
    **Available Tools:**
    - translate_content: Translate text between languages
    - check_visa_requirements: Verify visa and documentation needs
    - provide_cultural_guidance: Offer cultural tips and etiquette
    - calculate_time_zones: Time zone conversions and jet lag advice
    
    **Supported Languages:**
    - Major: English, Spanish, French, German, Italian, Portuguese
    - Asian: Chinese (Simplified/Traditional), Japanese, Korean, Thai
    - Middle East: Arabic, Hebrew, Turkish
    - Others: Russian, Hindi, Dutch, Swedish, Polish
    
    **State Management:**
    - Track language preference in state['preferred_language']
    - Store translations in state['translation_history']
    - Monitor visa status in state['visa_requirements']
    - Record cultural briefings in state['cultural_guidance']
    
    **Communication Guidelines:**
    - Be culturally sensitive and respectful
    - Avoid stereotypes or generalizations
    - Provide practical, actionable advice
    - Acknowledge cultural differences without judgment
    - Offer language assistance proactively
    
    **Visa Expertise:**
    - Schengen Area rules
    - Transit visa requirements
    - Business vs. tourist visas
    - Visa waiver programs
    - Online visa applications
    - Expedited processing options
    
    **Emergency Phrases (All Languages):**
    - Help / Emergency
    - Medical assistance needed
    - Police
    - Embassy
    - I don't speak [language]
    - Where is...?
    
    **Special Considerations:**
    - Religious dietary restrictions
    - Prayer time accommodations
    - Alcohol restrictions
    - Photography limitations
    - Sacred site protocols
    - Gender-specific rules
    
    Always provide accurate, up-to-date information and remind passengers
    to verify requirements with official sources. Be prepared to assist
    with language barriers during crisis situations.
    """,
    tools=[
        translate_content_tool,
        check_visa_requirements_tool,
        provide_cultural_guidance_tool,
        calculate_time_zones_tool
    ]
)