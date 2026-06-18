from botbuilder.core import CardFactory
from botbuilder.schema import Attachment


def build_after_feedback_card(text: str) -> dict:
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.6",
        "rtl": False,
        "body": [
            {"type": "TextBlock", "text": text, "wrap": True},
            {"type": "TextBlock", "wrap": True, "text": "Thank you for your feedback"},
        ],
    }


def make_after_feedback_card_attachment(text: str) -> Attachment:
    return CardFactory.adaptive_card(build_after_feedback_card(text=text))


def build_response_card(text: str, message_id: str, conversation_id: str) -> dict:
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.6",
        "rtl": False,
        "body": [
            {"type": "TextBlock", "text": text, "wrap": True},
            {
                "type": "ActionSet",
                "actions": [
                    {
                        "type": "Action.ShowCard",
                        "card": {
                            "type": "AdaptiveCard",
                            "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                            "version": "1.6",
                            "body": [
                                {
                                    "type": "Input.Text",
                                    "label": "Great! What did you like about this response?",
                                    "placeholder": "Tell us what you liked ...",
                                    "id": "positive-input",
                                    "isRequired": True,
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Submit Feedback",
                                    "data": {
                                        "actionName": "feedback",
                                        "actionValue": {
                                            "reaction": "like",
                                            "message_id": message_id,
                                            "conversation_id": conversation_id,
                                            "original_response": text,
                                            "feedback_type": "detailed",
                                        },
                                    },
                                }
                            ],
                        },
                        "title": "👍",
                    },
                    {
                        "type": "Action.ShowCard",
                        "card": {
                            "type": "AdaptiveCard",
                            "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
                            "version": "1.6",
                            "body": [
                                {
                                    "type": "Input.Text",
                                    "label": "Sorry to hear that. How can we improve?",
                                    "placeholder": "Tell us how we can improve...",
                                    "id": "negative-input",
                                    "isRequired": True,
                                }
                            ],
                            "actions": [
                                {
                                    "type": "Action.Submit",
                                    "title": "Submit Feedback",
                                    "data": {
                                        "actionName": "feedback",
                                        "actionValue": {
                                            "reaction": "dislike",
                                            "message_id": message_id,
                                            "conversation_id": conversation_id,
                                            "original_response": text,
                                            "feedback_type": "detailed",
                                        },
                                    },
                                }
                            ],
                        },
                        "title": "👎",
                    },
                ],
            },
        ],
    }


def make_card_attachment(
    text: str, message_id: str, conversation_id: str
) -> Attachment:
    return CardFactory.adaptive_card(
        build_response_card(text, message_id, conversation_id)
    )
