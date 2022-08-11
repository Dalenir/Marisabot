import os
from datetime import datetime

from aiogram.types import Update, Chat, User, Message, CallbackQuery


def fake_message_update(message_text: str, chat_id: int, user_id: int):
    return Update(
        update_id=1,
        message=Message(
            message_id=1,
            date=datetime.utcnow(),
            from_user=User(
                id=user_id,
                is_bot=False,
                first_name=''
            ),
            chat=Chat(
                id=chat_id,
                type="channel"
            ),
            text=f'{message_text}'
        )
    )


def fake_callback_update(data: str, chat_id: int, user_id: int):
    return Update(
        update_id=1,
        callback_query=CallbackQuery(
            id='1',
            from_user=User(
                id=user_id,
                is_bot=False,
                first_name=''
            ),
            chat_instance=str(chat_id),
            message=Message(
                message_id=1,
                date=datetime.utcnow(),
                from_user=User(
                    id=user_id,
                    is_bot=False,
                    first_name=''
                ),
                chat=Chat(
                    id=chat_id,
                    type="channel"
                ),
                text=''),
            data=data
            )
        )


fake_message = Message(
                message_id=1,
                date=datetime.utcnow(),
                from_user=User(
                    id=os.getenv('TEST_USER_ID'),
                    is_bot=False,
                    first_name=''
                ),
                chat=Chat(
                    id=os.getenv('TEST_USER_ID'),
                    type="private"
                ),
                text='txt'
                )
