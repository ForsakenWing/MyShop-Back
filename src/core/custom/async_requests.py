import json


async def post_async(url, session, body, headers=None):
    async with session.post(url=url, headers=headers, data=body) as response:
        text = await response.text()
        return json.loads(text)
