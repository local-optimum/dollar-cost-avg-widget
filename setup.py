import flask
from flask import request, jsonify
from coin_price_api import *

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Dollar Cost Averaging for Crypto</h1>
<p>An API that returns the results of dollar cost averaging when investing in crypto, based on coingecko prices.
Structure API call as /dca/query?coin=INPUT&deposit=INPUT&currency=INPUT&frequency=INPUT&startdate=INPUT</p>'''


@app.route('/dca/query', methods=['GET'])
def api_calc():
    if ('coin' and 'deposit' and 'currency' and 'frequency' and 'startdate')in request.args:
        results = costAverageFunc(request.args['coin'], request.args['deposit'], request.args['currency'], request.args['frequency'], request.args['startdate'])
        return jsonify(results)
    else:
        return "Error: incomplete query, please include coin name, deposit amount, currency, frequency and startdate."


app.run()

#http://127.0.0.1:5000/dca/query?coin=bitcoin&deposit=100&currency=usd&frequency=1&startdate=2021-01-05