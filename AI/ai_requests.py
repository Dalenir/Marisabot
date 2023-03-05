import datetime
import json
import os
import pickle
from json import JSONDecodeError
from typing import TypedDict

import asyncio
from aiogram.client.session import aiohttp
import tiktoken
from DBs.DBuse import redis_list, redis_add_to_list
from Marisa import data

with open('AI/ai_settings') as f:
    base_ai_rules = f.read()


async def make_request(url: str, method: str, headers, data=None):
    async with aiohttp.ClientSession() as session:
        valid = {'get', 'post', 'update', 'delete', 'patch'}
        if method not in valid:
            raise ValueError(f"results: status must be one of {valid}.")
        if method == 'post':
            async with session.post(url=url, data=data, headers=headers) as response:
                resp = await response.read()
                try:
                    return json.loads(resp)
                except JSONDecodeError:
                    print('There is no response')
                    return None
        elif method == 'get':
            async with session.get(url=url, data=data, headers=headers) as response:
                resp = await response.read()
                return json.loads(resp)
        elif method == 'patch':
            async with session.patch(url=url, data=data, headers=headers) as response:
                resp = await response.read()
                try:
                    return json.loads(resp)
                except JSONDecodeError:
                    print('There is no response')
                    return None


def num_tokens_from_messages(messages):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


class AIMessage(TypedDict):
    role: str
    content: str


async def afterward_tuning(messages: list[AIMessage],
                           user_message: AIMessage,
                           assistant_message: AIMessage,
                           redis_key: str):
    messages.append(user_message)
    messages.append(assistant_message)
    while num_tokens_from_messages(messages) > 4050:
        messages.pop(2)
    await redis_add_to_list(redis_key, pickle.dumps(user_message))
    await redis_add_to_list(redis_key, pickle.dumps(assistant_message))





async def ai_sentient_witch(new_text: str, user_id: int):
    redis_key = f"{user_id}: memory_dance"
    old_messages = list()
    memory = await redis_list(redis_key)
    if isinstance(memory, list) and memory:
        for mess in memory:
            ai_message = pickle.loads(mess)
            old_messages.append(ai_message)

    user_message = AIMessage(role="user", content=new_text)

    messages = [AIMessage(role="system", content=base_ai_rules)]
    messages.extend(old_messages[::-1])
    messages.append(user_message)

    tokens = num_tokens_from_messages(messages)
    while tokens > 4000:
        print(f'Need adjustment: {user_id}, tokens: {tokens}')
        messages.pop(2)
        tokens = num_tokens_from_messages(messages)

    res = await make_request(
        "https://api.openai.com/v1/chat/completions",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {data.aitoken}'
        },
        data=json.dumps({
          "model": "gpt-3.5-turbo",
          "messages": messages,
          "temperature": 0.7,
          "max_tokens": 1000,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0
        }),
        method='post'
    )
    print(user_id, res.get('usage'))
    real_answer = res.get('choices')[0].get("message").get("content")
    await asyncio.gather(afterward_tuning(messages,
                                 user_message=user_message,
                                 assistant_message=AIMessage(role='assistant', content=real_answer),
                                 redis_key=redis_key))
    return real_answer
