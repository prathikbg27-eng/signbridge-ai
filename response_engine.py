"""
SignBridge AI — Natural Contextual Response Engine
Understands recognized signs in the context of recent conversation history,
pending system questions, and conversational topics to generate natural, human-like responses.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time
import random


@dataclass
class ConversationTurn:
    id: str
    speaker: str  # "user" | "assistant"
    input_type: str  # "sign" | "text" | "voice"
    text: str
    sign: Optional[str] = None
    intent: Optional[str] = None
    confidence: Optional[float] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "speaker": self.speaker,
            "inputType": self.input_type,
            "text": self.text,
            "sign": self.sign,
            "intent": self.intent,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
        }


@dataclass
class ConversationContext:
    recent_turns: List[ConversationTurn] = field(default_factory=list)
    current_topic: Optional[str] = None
    current_intent: Optional[str] = None
    pending_question: Optional[str] = None
    pending_expected_responses: List[str] = field(default_factory=list)
    last_recognized_sign: Optional[str] = None
    last_system_message: Optional[str] = None
    greeting_count: int = 0

    def add_turn(self, turn: ConversationTurn, max_turns: int = 8):
        self.recent_turns.append(turn)
        if len(self.recent_turns) > max_turns:
            self.recent_turns.pop(0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recentTurns": [t.to_dict() for t in self.recent_turns],
            "currentTopic": self.current_topic,
            "currentIntent": self.current_intent,
            "pendingQuestion": self.pending_question,
            "pendingExpectedResponses": self.pending_expected_responses,
            "lastRecognizedSign": self.last_recognized_sign,
            "lastSystemMessage": self.last_system_message,
            "greetingCount": self.greeting_count,
        }


@dataclass
class ContextualResponse:
    text: str
    intent: str
    confidence: float
    response_gloss: List[str]
    response_type: str  # "contextual" | "direct" | "fallback"
    avatar_expression: str = "friendly"
    avatar_gesture: Optional[str] = None
    voice_enabled: bool = True
    new_pending_question: Optional[str] = None
    new_topic: Optional[str] = None
    new_expected_responses: List[str] = field(default_factory=list)

    @property
    def responseText(self) -> str:
        return self.text

    @property
    def responseGloss(self) -> List[str]:
        return self.response_gloss

    def to_dict(self) -> Dict[str, Any]:
        return {
            "responseText": self.text,
            "text": self.text,
            "intent": self.intent,
            "confidence": self.confidence,
            "responseGloss": self.response_gloss,
            "responseType": self.response_type,
            "avatarExpression": self.avatar_expression,
            "avatarGesture": self.avatar_gesture,
            "voiceEnabled": self.voice_enabled,
            "newPendingQuestion": self.new_pending_question,
            "newTopic": self.new_topic,
            "newExpectedResponses": self.new_expected_responses,
        }


def generate_natural_response(
    recognized_sign: str,
    context: Optional[ConversationContext] = None,
    confidence: float = 0.94,
) -> ContextualResponse:
    """
    Generates a natural conversational response based on the recognized sign,
    current pending questions, active topic, and recent conversation turns.
    """
    if context is None:
        context = ConversationContext()

    sign_upper = recognized_sign.upper().strip().replace(" ", "_")

    # Low confidence fallback
    if confidence < 0.70:
        return ContextualResponse(
            text="Sorry, I wasn't sure what that sign meant. Please try again.",
            intent="UNCERTAIN",
            confidence=confidence,
            response_gloss=[],
            response_type="fallback",
            avatar_expression="concerned",
        )

    pending_q = context.pending_question
    topic = context.current_topic

    # --------------------------------------------------------------------------
    # 1. GREETINGS (HELLO / HI / HEY / GOOD MORNING / GOOD EVENING)
    # --------------------------------------------------------------------------
    if sign_upper in ["HELLO", "HI", "HEY"]:
        if context.greeting_count > 0:
            return ContextualResponse(
                text="Hi again! What's on your mind?",
                intent="GREETING",
                confidence=confidence,
                response_gloss=["HELLO"],
                response_type="contextual",
                avatar_expression="friendly",
            )
        else:
            context.greeting_count += 1
            return ContextualResponse(
                text="Hello! What's up?",
                intent="GREETING",
                confidence=confidence,
                response_gloss=["HELLO"],
                response_type="direct",
                avatar_expression="friendly",
            )

    if sign_upper in ["GOOD_MORNING", "MORNING"]:
        return ContextualResponse(
            text="Good morning! How are you?",
            intent="GREETING",
            confidence=confidence,
            response_gloss=["GOOD", "DAY"],
            response_type="direct",
            avatar_expression="friendly",
            new_pending_question="HOW_ARE_YOU",
        )

    if sign_upper in ["GOOD_EVENING", "EVENING"]:
        return ContextualResponse(
            text="Good evening! How's it going?",
            intent="GREETING",
            confidence=confidence,
            response_gloss=["GOOD", "NIGHT"],
            response_type="direct",
            avatar_expression="friendly",
            new_pending_question="HOW_ARE_YOU",
        )

    # --------------------------------------------------------------------------
    # 2. CASUAL CONVERSATION (HOW ARE YOU)
    # --------------------------------------------------------------------------
    if sign_upper in ["HOW_ARE_YOU", "HOW"]:
        if sign_upper == "HOW_ARE_YOU" or pending_q == "HOW_ARE_YOU":
            return ContextualResponse(
                text="I'm doing well! How are you?",
                intent="CASUAL_CONVERSATION",
                confidence=confidence,
                response_gloss=["GOOD", "HOW"],
                response_type="direct",
                avatar_expression="friendly",
            )

    # --------------------------------------------------------------------------
    # 3. GRATITUDE (THANK YOU)
    # --------------------------------------------------------------------------
    if sign_upper in ["THANK_YOU", "THANKYOU", "THANKS"]:
        variations = ["You're welcome!", "Anytime! Happy to help.", "You're very welcome!"]
        chosen = variations[0] if len(context.recent_turns) == 0 else random.choice(variations)
        return ContextualResponse(
            text=chosen,
            intent="GRATITUDE",
            confidence=confidence,
            response_gloss=["WELCOME"],
            response_type="direct",
            avatar_expression="warm",
            new_pending_question=None,
        )

    # --------------------------------------------------------------------------
    # 4. REQUEST FOR HELP (HELP)
    # --------------------------------------------------------------------------
    if sign_upper == "HELP":
        return ContextualResponse(
            text="Of course! What do you need help with?",
            intent="REQUEST_HELP",
            confidence=confidence,
            response_gloss=["HELP", "HOW"],
            response_type="direct",
            avatar_expression="attentive",
            new_pending_question="WHAT_HELP_NEEDED",
            new_topic="HELP",
            new_expected_responses=["HOSPITAL", "DOCTOR", "WATER", "EMERGENCY", "WHERE", "YES", "NO"],
        )

    # --------------------------------------------------------------------------
    # 5. HOSPITAL
    # --------------------------------------------------------------------------
    if sign_upper == "HOSPITAL":
        if topic in ["HELP", "LOCATION", "EMERGENCY"] or pending_q in ["WHAT_HELP_NEEDED", "NEED_HELP"]:
            return ContextualResponse(
                text="Are you looking for the hospital?",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["HOSPITAL"],
                response_type="contextual",
                avatar_expression="attentive",
                new_pending_question="HOSPITAL_LOCATION",
                new_topic="HOSPITAL",
                new_expected_responses=["YES", "NO", "WHERE"],
            )
        else:
            return ContextualResponse(
                text="The hospital is located nearby. Stay calm, I'm here to help.",
                intent="REQUEST_LOCATION",
                confidence=confidence,
                response_gloss=["HOSPITAL"],
                response_type="direct",
                avatar_expression="attentive",
                new_topic="HOSPITAL",
            )

    # --------------------------------------------------------------------------
    # 6. DOCTOR
    # --------------------------------------------------------------------------
    if sign_upper == "DOCTOR":
        if topic in ["HELP", "EMERGENCY"] or pending_q == "WHAT_HELP_NEEDED":
            return ContextualResponse(
                text="Do you need a doctor right away?",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["DOCTOR", "HELP"],
                response_type="contextual",
                avatar_expression="serious",
                new_pending_question="DOCTOR_NEEDED",
                new_topic="DOCTOR",
                new_expected_responses=["YES", "NO"],
            )
        else:
            return ContextualResponse(
                text="Do you need medical attention or a doctor?",
                intent="REQUEST",
                confidence=confidence,
                response_gloss=["DOCTOR"],
                response_type="direct",
                avatar_expression="serious",
                new_pending_question="DOCTOR_NEEDED",
                new_topic="DOCTOR",
                new_expected_responses=["YES", "NO"],
            )

    # --------------------------------------------------------------------------
    # 7. YES (Context-Aware Confirmation)
    # --------------------------------------------------------------------------
    if sign_upper == "YES":
        if pending_q == "HOSPITAL_LOCATION" or topic == "HOSPITAL":
            return ContextualResponse(
                text="Okay. I can help with that.",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["GOOD", "HELP"],
                response_type="contextual",
                avatar_expression="attentive",
                new_topic="HOSPITAL",
            )
        elif pending_q == "OFFER_WATER" or topic == "WATER":
            return ContextualResponse(
                text="Sure, I'll get you some.",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["WATER"],
                response_type="contextual",
                avatar_expression="friendly",
                new_topic="WATER",
            )
        elif pending_q == "OFFER_FOOD" or topic == "FOOD":
            return ContextualResponse(
                text="Sure, I'll arrange some food for you.",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["FOOD"],
                response_type="contextual",
                avatar_expression="friendly",
                new_topic="FOOD",
            )
        elif pending_q in ["NEED_HELP", "WHAT_HELP_NEEDED"] or topic == "HELP":
            return ContextualResponse(
                text="Of course! What do you need help with?",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["HELP", "HOW"],
                response_type="contextual",
                avatar_expression="attentive",
                new_pending_question="WHAT_HELP_NEEDED",
                new_topic="HELP",
                new_expected_responses=["HOSPITAL", "DOCTOR", "WATER", "EMERGENCY", "WHERE"],
            )
        elif pending_q == "READY_TO_CONTINUE" or topic == "CONTINUE":
            return ContextualResponse(
                text="Great, let's continue.",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="friendly",
            )
        elif pending_q == "DOCTOR_NEEDED" or topic in ["DOCTOR", "MEDICAL", "EMERGENCY"]:
            return ContextualResponse(
                text="Understood. I will contact medical assistance for you.",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["DOCTOR", "HELP"],
                response_type="contextual",
                avatar_expression="serious",
                new_topic="MEDICAL",
            )
        else:
            # Standalone YES without prior context
            return ContextualResponse(
                text="Got it. How can I help?",
                intent="CONFIRMATION",
                confidence=confidence,
                response_gloss=["HOW", "HELP"],
                response_type="contextual",
                avatar_expression="friendly",
                new_pending_question="WHAT_HELP_NEEDED",
                new_topic="HELP",
            )

    # --------------------------------------------------------------------------
    # 8. NO (Context-Aware Denial)
    # --------------------------------------------------------------------------
    if sign_upper == "NO":
        if pending_q == "OFFER_WATER" or topic == "WATER":
            return ContextualResponse(
                text="No problem.",
                intent="DENIAL",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="friendly",
            )
        elif pending_q == "OFFER_FOOD" or topic == "FOOD":
            return ContextualResponse(
                text="No problem. Let me know if you get hungry later.",
                intent="DENIAL",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="friendly",
            )
        elif pending_q in ["NEED_HELP", "WHAT_HELP_NEEDED"] or topic == "HELP":
            return ContextualResponse(
                text="No problem. Let me know if you need anything.",
                intent="DENIAL",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="warm",
            )
        elif pending_q == "READY_TO_CONTINUE":
            return ContextualResponse(
                text="Take your time. Let me know when you are ready.",
                intent="DENIAL",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="warm",
            )
        else:
            return ContextualResponse(
                text="Understood. Let me know if you need anything.",
                intent="DENIAL",
                confidence=confidence,
                response_gloss=["GOOD"],
                response_type="contextual",
                avatar_expression="neutral",
            )

    # --------------------------------------------------------------------------
    # 9. WHAT (Context-Aware Question)
    # --------------------------------------------------------------------------
    if sign_upper in ["WHAT", "QUESTION"]:
        if topic == "HOSPITAL":
            return ContextualResponse(
                text="The hospital provides emergency medical care. Do you need directions?",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["HOSPITAL"],
                response_type="contextual",
                avatar_expression="attentive",
            )
        elif topic == "WATER":
            return ContextualResponse(
                text="I can get you clean drinking water.",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["WATER"],
                response_type="contextual",
                avatar_expression="friendly",
            )
        else:
            return ContextualResponse(
                text="What would you like to know? I'm here to assist.",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["QUESTION"],
                response_type="direct",
                avatar_expression="attentive",
            )

    # --------------------------------------------------------------------------
    # 10. WHERE (Context-Aware Location Question)
    # --------------------------------------------------------------------------
    if sign_upper == "WHERE":
        if topic == "HOSPITAL":
            return ContextualResponse(
                text="Yes, I can help you find the hospital. It's straight ahead.",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["HOSPITAL"],
                response_type="contextual",
                avatar_expression="attentive",
                new_topic="HOSPITAL",
            )
        elif topic in ["DOCTOR", "MEDICAL"]:
            return ContextualResponse(
                text="The medical clinic is straight down this corridor.",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["DOCTOR"],
                response_type="contextual",
                avatar_expression="attentive",
                new_topic="DOCTOR",
            )
        else:
            return ContextualResponse(
                text="Where would you like to go? I can give you directions.",
                intent="QUESTION",
                confidence=confidence,
                response_gloss=["QUESTION"],
                response_type="direct",
                avatar_expression="attentive",
                new_pending_question="ASK_LOCATION",
                new_topic="LOCATION",
            )

    # --------------------------------------------------------------------------
    # 11. WATER & FOOD (Requests)
    # --------------------------------------------------------------------------
    if sign_upper == "WATER":
        return ContextualResponse(
            text="Would you like some water?",
            intent="REQUEST",
            confidence=confidence,
            response_gloss=["WATER"],
            response_type="direct",
            avatar_expression="attentive",
            new_pending_question="OFFER_WATER",
            new_topic="WATER",
            new_expected_responses=["YES", "NO"],
        )

    if sign_upper == "FOOD":
        return ContextualResponse(
            text="Would you like some food or something to eat?",
            intent="REQUEST",
            confidence=confidence,
            response_gloss=["FOOD"],
            response_type="direct",
            avatar_expression="friendly",
            new_pending_question="OFFER_FOOD",
            new_topic="FOOD",
            new_expected_responses=["YES", "NO"],
        )

    # --------------------------------------------------------------------------
    # 12. EMERGENCY
    # --------------------------------------------------------------------------
    if sign_upper == "EMERGENCY":
        return ContextualResponse(
            text="Emergency assistance is on alert. What happened?",
            intent="EMERGENCY",
            confidence=confidence,
            response_gloss=["HELP"],
            response_type="direct",
            avatar_expression="serious",
            new_pending_question="DOCTOR_NEEDED",
            new_topic="EMERGENCY",
            new_expected_responses=["HOSPITAL", "DOCTOR", "YES", "NO"],
        )

    # --------------------------------------------------------------------------
    # 13. GOOD / BAD / PLEASE / SORRY / STOP / HOW
    # --------------------------------------------------------------------------
    if sign_upper == "GOOD":
        return ContextualResponse(
            text="Glad to hear that!",
            intent="CASUAL_CONVERSATION",
            confidence=confidence,
            response_gloss=["GOOD"],
            response_type="direct",
            avatar_expression="friendly",
        )

    if sign_upper == "BAD":
        return ContextualResponse(
            text="I'm sorry to hear that. How can I make it better?",
            intent="CASUAL_CONVERSATION",
            confidence=confidence,
            response_gloss=["HELP"],
            response_type="direct",
            avatar_expression="concerned",
            new_pending_question="WHAT_HELP_NEEDED",
            new_topic="HELP",
        )

    if sign_upper == "PLEASE":
        return ContextualResponse(
            text="Certainly! Whatever you need.",
            intent="REQUEST",
            confidence=confidence,
            response_gloss=["GOOD"],
            response_type="direct",
            avatar_expression="friendly",
        )

    if sign_upper == "SORRY":
        return ContextualResponse(
            text="No worries at all! Everything is okay.",
            intent="CASUAL_CONVERSATION",
            confidence=confidence,
            response_gloss=["GOOD"],
            response_type="direct",
            avatar_expression="warm",
        )

    if sign_upper == "STOP":
        return ContextualResponse(
            text="Stopping now. Standing by.",
            intent="REQUEST",
            confidence=confidence,
            response_gloss=["STOP"],
            response_type="direct",
            avatar_expression="neutral",
        )

    if sign_upper == "HOW":
        return ContextualResponse(
            text="I can explain how. What would you like to learn?",
            intent="QUESTION",
            confidence=confidence,
            response_gloss=["HOW"],
            response_type="direct",
            avatar_expression="attentive",
        )

    # Fallback
    return ContextualResponse(
        text=f"Got it. You signed {sign_upper}. How would you like to proceed?",
        intent="CASUAL_CONVERSATION",
        confidence=confidence,
        response_gloss=["GOOD"],
        response_type="fallback",
        avatar_expression="friendly",
    )


# Backward-compatible alias
generate_contextual_response = generate_natural_response
generateNaturalResponse = generate_natural_response
