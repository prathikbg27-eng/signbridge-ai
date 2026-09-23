"""
SignBridge AI — Action → Response Registry
Central configuration mapping recognized user hand signs to conversational AI intents,
avatar reactions, expressions, response gloss sequences, and vocal synthesis.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json


@dataclass
class ActionResponse:
    recognized_sign: str
    intent: str
    response_text: str
    response_gloss: List[str]
    avatar_expression: str = "friendly"
    avatar_gesture: Optional[str] = None
    voice_enabled: bool = True
    cooldown_ms: int = 2500

    def to_dict(self):
        return {
            "recognizedSign": self.recognized_sign,
            "intent": self.intent,
            "responseText": self.response_text,
            "responseGloss": self.response_gloss,
            "avatarExpression": self.avatar_expression,
            "avatarGesture": self.avatar_gesture,
            "voiceEnabled": self.voice_enabled,
            "cooldownMs": self.cooldown_ms,
        }


# Central Action → Response Registry
# The avatar determines a conversational response rather than simply mirroring the user's gesture.
ACTION_RESPONSES = {
    "HELLO": ActionResponse(
        recognized_sign="HELLO",
        intent="GREETING",
        response_text="Hi! 👋 Nice to communicate with you.",
        response_gloss=["HELLO"],
        avatar_expression="friendly",
        cooldown_ms=2500,
    ),
    "HI": ActionResponse(
        recognized_sign="HI",
        intent="GREETING",
        response_text="Hello! How are you doing today?",
        response_gloss=["HELLO"],
        avatar_expression="friendly",
        cooldown_ms=2500,
    ),
    "THANK_YOU": ActionResponse(
        recognized_sign="THANK_YOU",
        intent="GRATITUDE",
        response_text="You're very welcome! Happy to assist.",
        response_gloss=["WELCOME"],
        avatar_expression="warm",
        cooldown_ms=2500,
    ),
    "HELP": ActionResponse(
        recognized_sign="HELP",
        intent="REQUEST_HELP",
        response_text="How can I help you? I'm here.",
        response_gloss=["HELP", "HOW"],
        avatar_expression="attentive",
        cooldown_ms=3000,
    ),
    "EMERGENCY": ActionResponse(
        recognized_sign="EMERGENCY",
        intent="EMERGENCY_INTENT",
        response_text="How can I help you? Emergency assistance is on alert.",
        response_gloss=["HELP"],
        avatar_expression="serious",
        cooldown_ms=3000,
    ),
    "YES": ActionResponse(
        recognized_sign="YES",
        intent="AFFIRMATION",
        response_text="Okay, perfect.",
        response_gloss=["GOOD"],
        avatar_expression="friendly",
        cooldown_ms=2000,
    ),
    "NO": ActionResponse(
        recognized_sign="NO",
        intent="NEGATION",
        response_text="Understood. Let's try something else.",
        response_gloss=["GOOD"],
        avatar_expression="neutral",
        cooldown_ms=2000,
    ),
    "WATER": ActionResponse(
        recognized_sign="WATER",
        intent="REQUEST_RESOURCE",
        response_text="Would you like some water? Taking care of you.",
        response_gloss=["WATER"],
        avatar_expression="attentive",
        cooldown_ms=2500,
    ),
    "FOOD": ActionResponse(
        recognized_sign="FOOD",
        intent="REQUEST_RESOURCE",
        response_text="Would you like food or something to eat?",
        response_gloss=["EAT"],
        avatar_expression="friendly",
        cooldown_ms=2500,
    ),
    "PLEASE": ActionResponse(
        recognized_sign="PLEASE",
        intent="COURTESY",
        response_text="Certainly! Whatever you need.",
        response_gloss=["GOOD"],
        avatar_expression="friendly",
        cooldown_ms=2000,
    ),
    "SORRY": ActionResponse(
        recognized_sign="SORRY",
        intent="APOLOGY",
        response_text="No worries at all! Everything is okay.",
        response_gloss=["GOOD"],
        avatar_expression="warm",
        cooldown_ms=2000,
    ),
    "GOOD": ActionResponse(
        recognized_sign="GOOD",
        intent="POSITIVE_FEEDBACK",
        response_text="Glad to hear that!",
        response_gloss=["GOOD"],
        avatar_expression="happy",
        cooldown_ms=2000,
    ),
    "BAD": ActionResponse(
        recognized_sign="BAD",
        intent="NEGATIVE_FEEDBACK",
        response_text="I'm sorry to hear that. How can I make it better?",
        response_gloss=["SORRY", "HELP"],
        avatar_expression="concerned",
        cooldown_ms=2500,
    ),
    "WHERE": ActionResponse(
        recognized_sign="WHERE",
        intent="LOCATION_QUERY",
        response_text="Where would you like to go? I can give directions.",
        response_gloss=["WHERE"],
        avatar_expression="attentive",
        cooldown_ms=2500,
    ),
    "HOW": ActionResponse(
        recognized_sign="HOW",
        intent="METHOD_QUERY",
        response_text="I can explain how. What would you like to learn?",
        response_gloss=["HOW"],
        avatar_expression="attentive",
        cooldown_ms=2500,
    ),
    "STOP": ActionResponse(
        recognized_sign="STOP",
        intent="HALT_INSTRUCTION",
        response_text="Stopping now.",
        response_gloss=["STOP"],
        avatar_expression="neutral",
        cooldown_ms=2000,
    ),
    "DOCTOR": ActionResponse(
        recognized_sign="DOCTOR",
        intent="MEDICAL_REQUEST",
        response_text="Do you need a doctor or medical attention?",
        response_gloss=["HELP", "HOSPITAL"],
        avatar_expression="serious",
        cooldown_ms=3000,
    ),
    "HOSPITAL": ActionResponse(
        recognized_sign="HOSPITAL",
        intent="MEDICAL_REQUEST",
        response_text="The hospital is located straight ahead. Stay calm.",
        response_gloss=["HOSPITAL"],
        avatar_expression="attentive",
        cooldown_ms=3000,
    ),
}


def get_action_response(sign: str) -> Optional[ActionResponse]:
    """Retrieves the conversational response definition for a recognized user sign."""
    if not sign:
        return None
    normalized_key = sign.strip().upper().replace(" ", "_")
    return ACTION_RESPONSES.get(normalized_key)


def export_action_responses_json() -> str:
    """Serializes the registry into JSON for embedding into client-side JS."""
    return json.dumps({k: v.to_dict() for k, v in ACTION_RESPONSES.items()})
