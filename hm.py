import twitchio
from twitchio.ext import commands
from openai import OpenAI
import os
from gtts import gTTS

# change these into your api key

API_KEY = ''
CHANNEL_NAME = ''
THREAD_ID = ''
ASSISTANT_ID = ''
TWITCH_OAUTH_TOKEN = ''

client = OpenAI(api_key = API_KEY)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TWITCH_OAUTH_TOKEN, prefix='!', initial_channels=[CHANNEL_NAME])

    async def event_ready(self):
        print(f'Logged in as {self.nick}')

    # shit what tts shoul I use brahhhhh
    def tts(self, text):
            tts = gTTS(text=text, lang='en-AU')
            tts_file = 'tts.mp3'
            tts.save(tts_file)
            os.system(f"mpg123 {tts_file}")

# recieve message and pass to the gpt in liveee.
    async def event_message(self, message):
        print(f'[{message.author.name}]: {message.content}')

        if message.content.startswith('!hello'):
            await message.channel.send(f'Hello, {message.author.name}!')


        my_speech = message.content

        message = client.beta.threads.messages.create(
            thread_id=THREAD_ID,
            role="user",
            content=my_speech
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=THREAD_ID,
            assistant_id=ASSISTANT_ID
        )

        if run.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=THREAD_ID
            )
            
            print('[LLM]: ' + messages.data[0].content[0].text.value)
        else:
            print(run.status)

        text_to_speech = messages.data[0].content[0].text.value  # Extract text to convert to speech
        self.tts(text_to_speech)

bot = Bot()
bot.run()
