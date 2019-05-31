from flask import Flask, jsonify, request
from flask_cors import CORS
from housingdata import getapartments

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# sanity check route
@app.route('/list/', methods=['GET'])
def ping_pong():
    url = request.args.get('URL', '')
    csv = getapartments(url)
    return jsonify({
        'status': 'success',
        'csv': csv})


if __name__ == '__main__':
    app.run()
