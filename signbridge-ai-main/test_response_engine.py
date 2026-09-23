"""
Unit tests for the Natural Contextual Response Engine in SignBridge AI
"""

import unittest
from response_engine import (
    ConversationContext,
    ConversationTurn,
    generate_natural_response,
)


class TestNaturalResponseEngine(unittest.TestCase):

    def test_greeting_hello_what_is_up(self):
        # User: HI / HELLO -> "Hello! What's up?"
        ctx = ConversationContext(greeting_count=0)
        resp = generate_natural_response("HI", ctx)
        self.assertEqual(resp.text, "Hello! What's up?")
        self.assertEqual(resp.intent, "GREETING")
        self.assertEqual(resp.response_gloss, ["HELLO"])

        resp_hello = generate_natural_response("HELLO", ConversationContext(greeting_count=0))
        self.assertEqual(resp_hello.text, "Hello! What's up?")

    def test_good_morning_and_evening(self):
        # GOOD MORNING -> "Good morning! How are you?"
        resp1 = generate_natural_response("GOOD_MORNING")
        self.assertEqual(resp1.text, "Good morning! How are you?")
        self.assertEqual(resp1.intent, "GREETING")

        # GOOD EVENING -> "Good evening! How's it going?"
        resp2 = generate_natural_response("GOOD_EVENING")
        self.assertEqual(resp2.text, "Good evening! How's it going?")
        self.assertEqual(resp2.intent, "GREETING")

    def test_how_are_you(self):
        # HOW ARE YOU -> "I'm doing well! How are you?"
        resp = generate_natural_response("HOW_ARE_YOU")
        self.assertEqual(resp.text, "I'm doing well! How are you?")
        self.assertEqual(resp.intent, "CASUAL_CONVERSATION")

    def test_help_request(self):
        # HELP -> "Of course! What do you need help with?"
        resp = generate_natural_response("HELP")
        self.assertEqual(resp.text, "Of course! What do you need help with?")
        self.assertEqual(resp.intent, "REQUEST_HELP")
        self.assertIn("HELP", resp.response_gloss)

    def test_multi_turn_hi_help_hospital_yes(self):
        # Turn 1: User HI -> "Hello! What's up?"
        ctx = ConversationContext()
        r1 = generate_natural_response("HI", ctx)
        self.assertEqual(r1.text, "Hello! What's up?")
        ctx.current_topic = r1.new_topic
        ctx.pending_question = r1.new_pending_question

        # Turn 2: User HELP -> "Of course! What do you need help with?"
        r2 = generate_natural_response("HELP", ctx)
        self.assertEqual(r2.text, "Of course! What do you need help with?")
        ctx.current_topic = r2.new_topic
        ctx.pending_question = r2.new_pending_question

        # Turn 3: User HOSPITAL -> "Are you looking for the hospital?"
        r3 = generate_natural_response("HOSPITAL", ctx)
        self.assertEqual(r3.text, "Are you looking for the hospital?")
        self.assertEqual(r3.intent, "QUESTION")
        ctx.current_topic = r3.new_topic
        ctx.pending_question = r3.new_pending_question

        # Turn 4: User YES -> "Okay. I can help with that."
        r4 = generate_natural_response("YES", ctx)
        self.assertEqual(r4.text, "Okay. I can help with that.")
        self.assertEqual(r4.intent, "CONFIRMATION")

    def test_water_and_yes_context(self):
        # User: WATER -> "Would you like some water?" -> User: YES -> "Sure, I'll get you some."
        ctx = ConversationContext()
        r1 = generate_natural_response("WATER", ctx)
        self.assertEqual(r1.text, "Would you like some water?")
        ctx.current_topic = r1.new_topic
        ctx.pending_question = r1.new_pending_question

        r2 = generate_natural_response("YES", ctx)
        self.assertEqual(r2.text, "Sure, I'll get you some.")
        self.assertEqual(r2.intent, "CONFIRMATION")

    def test_water_and_no_context(self):
        # User: WATER -> "Would you like some water?" -> User: NO -> "No problem."
        ctx = ConversationContext()
        r1 = generate_natural_response("WATER", ctx)
        ctx.current_topic = r1.new_topic
        ctx.pending_question = r1.new_pending_question

        r2 = generate_natural_response("NO", ctx)
        self.assertEqual(r2.text, "No problem.")
        self.assertEqual(r2.intent, "DENIAL")

    def test_standalone_yes_and_no(self):
        # YES without context -> "Got it. How can I help?"
        r_yes = generate_natural_response("YES", ConversationContext())
        self.assertEqual(r_yes.text, "Got it. How can I help?")

        # NO without context -> "Understood. Let me know if you need anything."
        r_no = generate_natural_response("NO", ConversationContext())
        self.assertEqual(r_no.text, "Understood. Let me know if you need anything.")

    def test_thank_you(self):
        # THANK_YOU -> "You're welcome!" (or warm variation)
        resp = generate_natural_response("THANK_YOU")
        self.assertEqual(resp.intent, "GRATITUDE")
        self.assertIn("WELCOME", resp.response_gloss)

    def test_where_contextual(self):
        # WHERE with hospital topic
        ctx = ConversationContext(current_topic="HOSPITAL")
        resp = generate_natural_response("WHERE", ctx)
        self.assertIn("find the hospital", resp.text.lower())
        self.assertEqual(resp.intent, "QUESTION")

    def test_what_contextual(self):
        # WHAT with hospital topic
        ctx = ConversationContext(current_topic="HOSPITAL")
        resp = generate_natural_response("WHAT", ctx)
        self.assertIn("hospital", resp.text.lower())
        self.assertEqual(resp.intent, "QUESTION")


if __name__ == "__main__":
    unittest.main()
