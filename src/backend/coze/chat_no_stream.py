"""
This example describes how to use the chat interface to initiate conversations,
poll the status of the conversation, and obtain the messages after the conversation is completed.
"""

import json
import logging
import os
import time
from typing import Optional

from cozepy import COZE_CN_BASE_URL, ChatStatus, Coze, DeviceOAuthApp, Message, MessageType, TokenAuth
from cozepy.log import setup_logging


def get_coze_api_base() -> str:
    # The default access is api.coze.cn, but if you need to access api.coze.com,
    # please use base_url to configure the api endpoint to access
    coze_api_base = os.getenv("COZE_API_BASE")
    if coze_api_base:
        return coze_api_base

    return COZE_CN_BASE_URL  # default

def coze_chat_no_stream(coze_api_token: str, bot_id: str, user_id: str, additional_messages: list[Message]) -> list[Message]:
    """
    Call the coze.chat.create_and_poll method to create a chat. The create method is a non-streaming
    chat and will return a Chat class. Developers should periodically check the status of the
    chat and handle them separately according to different states.
    """
    # coze_api_token = 'pat_NASLTPBwiQfezRQ5zQV2dehJD87GKrQ6j20rlIQ2muiqEQH3Nwq52LhAgKwWL35O'
    coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=get_coze_api_base())

    chat = coze.chat.create(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=additional_messages
    )
    
    start = int(time.time())
    timeout = 600
    while chat.status == ChatStatus.IN_PROGRESS:
        if int(time.time()) - start > timeout:
            # too long, cancel chat
            coze.chat.cancel(conversation_id=chat.conversation_id, chat_id=chat.id)
            break

        time.sleep(1)
        # Fetch the latest data through the retrieve interface
        chat = coze.chat.retrieve(conversation_id=chat.conversation_id, chat_id=chat.id)

    # When the chat status becomes completed, all messages under this chat can be retrieved through the list messages interface.
    messages = coze.chat.messages.list(conversation_id=chat.conversation_id, chat_id=chat.id)
    for message in messages:
        print(f"role={message.role}, type={message.type}, content={message.content}")
        if message.type == MessageType.ANSWER:
            print(message.content, end="", flush=True)
    return messages


if __name__ == '__main__':
    bot_id = '7481110193267326991'
    user_id = 'albertym'
    additional_messages = [
        Message.build_user_question_text("你好"),
    ]
    message = coze_chat_no_stream(bot_id, user_id, additional_messages)

