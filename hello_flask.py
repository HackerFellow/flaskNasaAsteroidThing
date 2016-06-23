#!/usr/bin/env python

from secret import nasa_key
import urllib.request
import sys
import datetime
import flask
import json

def asteriods(start,end):
    url = 'https://api.nasa.gov/neo/rest/v1/feed?start_date=%s&end_date=%s&api_key=%s' % (start,end,nasa_key)
    print(url, file=sys.stderr)
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            data = json.loads(the_page.decode('utf-8'))
    except urllib.error.HTTPError:
        print("HTTP ERROR", file=sys.stderr)
        return -1;
    # print(data)
    return data

# Create the application.
APP = flask.Flask(__name__)


@APP.route('/<start>/<end>')
def search(start,end):
    """ Displays the index page accessible at '/'
    """

    startDate = datetime.datetime.strptime(start, "%Y-%m-%d").date();
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d").date();
    asteroids = asteriods(start,end);
    return flask.render_template('search.html', asteroids=asteroids, jsonDump=json.dumps(asteroids,sort_keys=True, indent=4))

@APP.route('/')
def index():
    return flask.render_template('index.html')

@APP.route('/hello/<name>/')
def hello(name):
    """
    Displays the page and greets whoever comes to visit it.
    """
    return flask.render_template('hello.html', name=name)


if __name__ == '__main__':
    APP.debug = True
    APP.run()
