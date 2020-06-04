import json
import requests

def get_results(query = 'data'):

    query = query.upper()

    # with open('sampleResponse', 'r') as f:
    # j = json.loads(f.read())
    courses_req = requests.get('https://sis.rutgers.edu/soc/api/courses.gzip?year=2020&term=9&campus=CM')
    j = json.loads(courses_req.text)

    # with open('openSec', 'r') as openS:
        # openSections = json.loads(openS.read())
    open_req = requests.get('https://sis.rutgers.edu/soc/api/openSections.gzip?year=2020&term=9&campus=CM')
    open_sections = json.loads(open_req.text)


    for i in j:
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

                if idx in open_sections:
                    print(f'{ idx }    { title }    OPEN')#    { start_time }    { end_time }')
                else:
                    print(f'{ idx }    { title }    CLOSED')#    { start_time }  { end_time }')

get_results()
