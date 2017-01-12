# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
import status_fetcher
import song_writer
import json

app = Flask(__name__)
app.config['DEBUG'] = True


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/get_song/', methods=['GET'])
def get_song():
    statuses = status_fetcher.get_statuses_content()
    writer = song_writer.SongWriter(material=statuses)
    song = writer.write()
    title = writer.get_song_title()
    song = song.replace('\n', '<br>')
    return json.dumps(
        {'title': title + u' / חברי וחברות הכנסת ה-20', 'content': song})


@app.route('/', methods=['GET'])
def main():
    """Return a friendly HTTP greeting."""
    return render_template('main.html')
    # return u'<p>song:<br>{}</p>'.format(song)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
