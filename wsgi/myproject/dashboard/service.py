from . import config
from . import private
from datetime import datetime
import json
import math
import requests


def get_user_data():
    user_url = 'https://habitica.com/api/v3/user'
    user_tasks_url = 'https://habitica.com/api/v3/tasks/user'

    users = private.USERS
    user_list = []

    for user in users:
        headers = {'x-api-user': user['user_id'],
                   'x-api-key': user['api_token']}

        user_rsp = json.loads(requests.get(user_url, headers=headers).text)
        user_tasks_rsp = json.loads(requests.get(user_tasks_url, headers=headers).text)

        user_data = user_rsp['data']
        user_data['health'] = int(round(user_data['stats']['hp']))
        gold, silver = get_formatted_gp(user_data['stats']['gp'])
        user_data['gold'] = gold
        user_data['silver'] = silver


        task_data = user_tasks_rsp['data']
        dailies, habits, todos = categorize_tasks(task_data)
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
    users = private.USERS

    headers = {'x-api-user': users[0]['user_id'],
				'x-api-key': users[0]['api_token']}

    chat_url = 'https://habitica.com/api/v3/groups/party/chat'

    chat_rsp = json.loads(requests.get(chat_url, headers=headers).text)

    chat_data = chat_rsp['data']
    chat_list = [d['text'] for d in chat_data]

    return chat_list

def score_task(user_id, task_id):
    api_token = get_api_token(user_id)
    headers = {'x-api-user': user_id,
               'x-api-key': api_token}

    score_url = 'https://habitica.com/api/v3/tasks/%s/score/up' % task_id
    task_rsp = json.loads(requests.post(score_url, headers=headers).text)

    discovery_msg = 'Although no items were found, you found greater confidence in doing a good deed.'

    if 'drop' in task_rsp['data']['_tmp']:
		discovery_msg = task_rsp['data']['_tmp']['drop']['dialog']

    result_msg = 'You worked hard! %s Also, check your stats for your progress. :)' % discovery_msg

    return result_msg


def get_api_token(user_id):
    for user in private.USERS:
        if user['user_id'] == user_id:
            return user['api_token']

    return None
