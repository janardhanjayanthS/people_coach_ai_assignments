# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from ai import get_people_coach_ai_response, post_message_feedback
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import Activity, ChannelAccount
from card import make_after_feedback_card_attachment, make_card_attachment
from log import get_logger

logger = get_logger(__name__)


class MyBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.value:
            await self._handle_feedback(turn_context)
            return

        user_text = turn_context.activity.text
        logger.info(f"User message: {user_text}")

        ai_response = get_people_coach_ai_response(query=user_text)
        if ai_response:
            logger.info(f"AI response: {ai_response['text']}")
            attachment = make_card_attachment(
                text=ai_response["text"],
                message_id=ai_response["message_id"],
                conversation_id=ai_response["conversation_id"],
            )
            await turn_context.send_activity(MessageFactory.attachment(attachment))
        else:
            await turn_context.send_activity(
                "Sorry, I couldn't get a response right now. Please try again."
            )

    async def _handle_feedback(self, turn_context: TurnContext):
        value = turn_context.activity.value
        action_name = value.get("actionName")

        if action_name != "feedback":
            logger.info(f"Unhandled action: {action_name}")
            return

        action_value = value.get("actionValue", {})
        reaction = action_value.get("reaction")
        positive = reaction == "like"
        reason = (
            value.get("positive_feedback")
            if positive
            else value.get("negative_feedback", "")
        )

        logger.info(f"Feedback received: reaction={reaction} reason={reason}")

        conversation_id = action_value.get("conversation_id")
        message_id = action_value.get("message_id")

        logger.debug(f"Conv. ID: {conversation_id}")
        logger.debug(f"Message ID: {message_id}")

        post_message_feedback(
            conversation_id=action_value.get("conversation_id", ""),
            message_id=action_value.get("message_id", ""),
            positive=positive,
            reason=reason or "",
        )

        updated_activity = Activity(
            id=turn_context.activity.reply_to_id,
            type="message",
            attachments=[
                make_after_feedback_card_attachment(
                    text=action_value["original_response"]
                )
            ],
        )

        await turn_context.update_activity(updated_activity)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
