import json
import os
import pickle
from json import JSONDecodeError
from typing import TypedDict

from aiogram.client.session import aiohttp

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

class AIMessage(TypedDict):
    role: str
    content: str


async def ai_sentient_witch(new_text: str, user_id: int):
    redis_key = f"{user_id}: memory_dance"
    old_messages = list()
    memory = await redis_list(redis_key)
    if isinstance(memory, list) and memory:
        for mess in memory:
            ai_message = pickle.loads(mess)
            old_messages.append(ai_message)

    messages = [AIMessage(role="system", content=base_ai_rules)]
    messages.extend(old_messages[::-1])
    messages.append(AIMessage(role="user", content=new_text))

    res = await make_request(
        "https://api.openai.com/v1/chat/completions",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {data.aitoken}'
        },
        data=json.dumps({
          "model": "gpt-3.5-turbo-0301",
          "messages": messages,
          "temperature": 0.7,
          "max_tokens": 1000,
          "top_p": 1,
          "frequency_penalty": 0,
          "presence_penalty": 0
        }),
        method='post'
    )
    real_answer = res.get('choices')[0].get("message").get("content")
    await redis_add_to_list(redis_key, pickle.dumps(AIMessage(role="user", content=new_text)))
    await redis_add_to_list(redis_key, pickle.dumps(AIMessage(role="assistant", content=real_answer)))
    return real_answer
