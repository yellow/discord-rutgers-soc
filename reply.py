import discord
import json
import requests
import aiohttp
import asyncio
import time

class MyClient(discord.Client):
    def __init__(self):
        #self.get_data()
        asyncio.get_event_loop().run_until_complete(self.get_data())
        super().__init__()


    async def get_data(self):
        print("Entered get_data()")
        async with aiohttp.ClientSession() as session:
            async with session.get('https://sis.rutgers.edu/soc/api/courses.gzip?year=2020&term=9&campus=CM') as courses_req:
                self.j = await courses_req.json(content_type=None)
            async with session.get('https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=CM') as open_req:
                self.open_sections = await open_req.json(content_type=None)
        print('Data downloaded and parsed successfully')

        self.last_time = time.time()

    async def get_results(self, query):
        if(time.time() - self.last_time > 3600):
            self.get_data()

        output = []
        query = query.upper()

        #courses_req = requests.get('https://sis.rutgers.edu/soc/api/courses.gzip?year=2020&term=9&campus=CM')
        #j = json.loads(courses_req.text)

        # with open('openSec', 'r') as openS:
        # openSections = json.loads(openS.read())
        #open_req = requests.get('https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=CM')
        #open_sections = json.loads(open_req.text)


        for i in self.j:
            title = i['title']
            if query in title:
                # with open(query, 'w') as op:
                    # op.write(json.dumps(i))
                for section in i['sections']:
                    idx = section['index']
                    # start_time = section['meetingTimes'][0]['startTime']#[:2] + ':' + section['meetingTimes']['startTime'][2:]
                    # end_time = section['meetingTimes'][0]['endTime']#[:2] + ':' + section['meetingTimes']['endTime'][2:]
                    # if not start_time:
                        # start_time = '-'
                    # if not end_time:
                        # end_time = '-'

                    if idx in self.open_sections:
                        output.append(f'{ idx }    { title }    OPEN')#    { start_time }    { end_time }')
                    else:
                        output.append(f'{ idx }    { title }    CLOSED')#    { start_time }  { end_time }')
        return '\n'.join(output)


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!course '):
            course_name = ' '.join(message.content.split(' ')[1:])
            output = await self.get_results(course_name)
            
            await message.channel.send(f'Hello { message.author.mention} \n { output }')

with open("token", 'r') as tk:
    token = tk.read().strip()
client = MyClient()
client.run(token)
