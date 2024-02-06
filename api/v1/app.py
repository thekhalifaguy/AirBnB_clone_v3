#!/usr/bin/python3
'''
Createw Flask app; and register the blueprint app_views to Flask instance app.
'''

from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# enable CORS and allow for origins:
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    '''
    Removes the current SQLAlchemy Session object after each request.
    '''
    storage.close()


# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    '''
    Return errmsg `Not Found`.
    '''
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)

api/v1/views/__init__.py

#!/usr/bin/python3
'''
Creates a Blueprint instance with `url_prefix` set to `/api/v1`.
'''


from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *

