import datetime
import urllib2
import json

KIKAR_API_PATH = 'http://kikar.org/api/v1/facebook_status/'

NUM_OF_STATUSES = 100

def get_yesterday():
    return (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(
        '%Y-%m-%d')


def request_statuses(num_of_statuses):
    url = KIKAR_API_PATH + '?limit={}&is_current=true&published__gte='.format(
        num_of_statuses) + get_yesterday()
    res = urllib2.urlopen(url)
    return json.loads(res.read())


def get_statuses_content(num_of_statuses=NUM_OF_STATUSES):
    response = request_statuses(num_of_statuses)
    return [status['content'] for status in
            response['objects'][:num_of_statuses]]
