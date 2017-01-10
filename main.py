from flask import Flask
import status_fetcher
import song_writer

app = Flask(__name__)
app.config['DEBUG'] = True

NUM_OF_STATUSES = 20

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    statuses = status_fetcher.get_statuses_content(NUM_OF_STATUSES)
    writer = song_writer.SongWriter(material=statuses)
    song = writer.write()
    return u'<p>song:<br>{}</p>'.format(song)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
