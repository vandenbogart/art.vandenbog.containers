import faust
from faustapp.app import app

topic = app.topic('user_data')


@app.agent(topic)
async def process(stream):
    async for user in stream:
        print(user)

