import requests
import datetime

KIKAR_API_PATH = 'http://kikar.org/api/v1/facebook_status/'


def get_yesterday():
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        '%Y-%m-%d')


def request_statuses():
    params = {'is_current': 'true',
              'published__gte': get_yesterday()
              }
    res = requests.get(KIKAR_API_PATH, params=params)
    return res.json()


def get_statuses_content():
    response = request_statuses()
    return [status['content'] for status in response['objects']]
