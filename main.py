# -*- coding: utf-8 -*-

import json
import hashlib

from flask import Flask
from flask import render_template
from flask.ext.dotenv import DotEnv
from flask_redis import FlaskRedis

import status_fetcher
import song_writer
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
env = DotEnv(app)
redis_store = FlaskRedis(app, strict=False)


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/get_song/', methods=['GET'])
def get_new_song():
    statuses = status_fetcher.get_statuses_content()
    writer = song_writer.SongWriter(material=statuses)
    song = writer.write()
    song_hash = hash_song(song)
    success = redis_store.set(song_hash, song.encode('utf8'))
    logger.info("save song:", success)
    return render_song(song, writer, song_hash, is_new=True)


@app.route('/<song_hash>/get_song/', methods=['GET'])
def get_hashed_song(song_hash):
    song = redis_store.get("{}".format(song_hash)).decode('utf8')
    writer = song_writer.SongWriter(material=[])
    return render_song(song, writer, song_hash, is_new=False)


def render_song(song, writer, link, is_new):
    title = writer.get_song_title(song)
    song = song.replace('\n', '<br>')
    return json.dumps(
        {'title': title + u' / חברי וחברות הכנסת ה-20', 'content': song,
         'link': str(link),
         'is_new': is_new})


def hash_song(song):
    sha1 = hashlib.sha1()
    sha1.update(song.encode('utf8'))
    return sha1.hexdigest()


@app.route('/', methods=['GET'])
def main():
    """Return a friendly HTTP greeting."""
    return render_template('main.html')


@app.route('/<song_hash>/', methods=['GET'])
def existing_song(song_hash):
    """Return a friendly HTTP greeting."""
    return render_template('main.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.before_request
def add_trailing():
    from flask import redirect, request

    request_path = request.path
    if not request_path.endswith('/'):
        return redirect(request_path + '/')


if __name__ == "__main__":
    app.run()
