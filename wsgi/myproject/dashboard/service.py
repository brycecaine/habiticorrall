from . import config
from .models import Person
from datetime import datetime
from pprint import pprint
import json
import math
import requests


def get_tasks(username):
    dailies = []
    habits = []
    todos = []

    if username:
        user_tasks_url = 'https://habitica.com/api/v3/tasks/user'

        person = Person.objects.get(username=username)
        headers = {'x-api-user': person.user_id,
                   'x-api-key': person.api_token}
        user_tasks_rsp = json.loads(requests.get(user_tasks_url, headers=headers).text)
        task_data = user_tasks_rsp['data']

        dailies, habits, todos = categorize_tasks(task_data)

        return (dailies, habits, todos)


def get_items(username):
    dailies = []
    habits = []
    todos = []

    if username:
        user_url = 'https://habitica.com/api/v3/user'

        person = Person.objects.get(username=username)
        headers = {'x-api-user': person.user_id,
                   'x-api-key': person.api_token}
        user_rsp = json.loads(requests.get(user_url, headers=headers).text)
        user_data = user_rsp['data']

        user_data['health'] = int(round(user_data['stats']['hp']))
        gold, silver = get_formatted_gp(user_data['stats']['gp'])
        user_data['gold'] = gold
        user_data['silver'] = silver

        return user_data


def get_user_data():
    user_url = 'https://habitica.com/api/v3/user'

    persons = Person.objects.all()
    user_list = []

    for person in persons:
        headers = {'x-api-user': person.user_id,
                   'x-api-key': person.api_token}

        user_rsp = json.loads(requests.get(user_url, headers=headers).text)

        user_data = user_rsp['data']
        user_data['health'] = int(round(user_data['stats']['hp']))
        gold, silver = get_formatted_gp(user_data['stats']['gp'])
        user_data['gold'] = gold
        user_data['silver'] = silver


        dailies, habits, todos = get_tasks(person.username)
        user_data['dailies'] = dailies
        user_data['habits'] = habits
        user_data['todos'] = todos

        user_list.append(user_data)

    return user_list


def categorize_tasks(task_data):
    dailies = []
    habits = []
    todos = []
    dailies_sorted = []
    habits_sorted = []
    todos_sorted = []

    for task in task_data:
        for task_color in config.TASK_COLORS:
            if task_color['min'] <= task['value'] <= task_color['max']:
                task['color'] = task_color['hex']
                break

        if task['type'] == 'daily':
            dailies.append(task)

        elif task['type'] == 'habit':
            habits.append(task)

        elif task['type'] == 'todo':
            if not task['completed']:
                todos.append(task)

        dailies_sorted = sorted(dailies, key=lambda k: k['text'])
        habits_sorted = sorted(habits, key=lambda k: k['text'])
        todos_sorted = sorted(todos, key=lambda k: k['text'])

    return (dailies_sorted, habits_sorted, todos_sorted)


def get_formatted_gp(gp):
	gold_fraction, gold = math.modf(gp)

	gold = int(gold)
	silver = int((int(gold_fraction * 100) / float(100)) * 100)

	return (gold, silver)


def get_chat_data():
    persons = Person.objects.all()

    headers = {'x-api-user': persons[0].user_id,
				'x-api-key': persons[0].api_token}

    chat_url = 'https://habitica.com/api/v3/groups/party/chat'

    chat_rsp = json.loads(requests.get(chat_url, headers=headers).text)

    chat_data = chat_rsp['data']
    chat_list = [d['text'] for d in chat_data]

    return chat_list

def score_task(username, task_id, direction='up'):
    person = Perons.objects.get(username=username)
    headers = {'x-api-user': person.user_id,
               'x-api-key': person.api_token}

    score_url = 'https://habitica.com/api/v3/tasks/%s/score/%s' % (
        task_id, direction)
    task_rsp = json.loads(requests.post(score_url, headers=headers).text)

    discovery_msg = 'Although no items were found, you found greater confidence in doing a good deed.'

    if 'drop' in task_rsp['data']['_tmp']:
		discovery_msg = task_rsp['data']['_tmp']['drop']['dialog']

    result_msg = 'You worked hard! %s Also, check your stats for your progress. :)' % discovery_msg

    return result_msg


def get_persons():
    persons = Person.objects.all()

    return persons


def get_person(username):
    person = Person.objects.get(username=username)

    return person
