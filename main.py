from flask import Flask
from flask import render_template
import status_fetcher
import song_writer

app = Flask(__name__)
app.config['DEBUG'] = True

NUM_OF_STATUSES = 100


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=['GET'])
def main():
    """Return a friendly HTTP greeting."""
    statuses = status_fetcher.get_statuses_content(NUM_OF_STATUSES)
    writer = song_writer.SongWriter(material=statuses)
    song = writer.write()
    title = writer.get_song_title()
    song = song.replace('\n', '<br>')
    return render_template('main.html', **{'song': song, 'title': title})
    # return u'<p>song:<br>{}</p>'.format(song)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
