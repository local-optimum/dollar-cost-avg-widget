import flask
from flask import request, jsonify
import requests
import datetime as dt
import pandas as pd

def costAverageFunc(coin, deposit, currency, frequency, startdate):
    """function that takes the above strings as inputs, converts them into an API query to coingecko
    then creates a dataframe of dollar cost averaging results vs a single deposit return"""

    #cleaning of inputs
    id = coin
    dep_amount = int(deposit)
    vs_currency = currency
    frequency = int(frequency)
    start_date = dt.datetime.strptime(startdate, "%Y-%m-%d").date()
    frequency_days = frequency*7

    #default end date
    today_date = dt.date.today()
    #default interval time
    interval = "daily"

    days = (today_date-start_date).days

    params = {"id": id, "vs_currency": vs_currency, "days": days, "interval": interval}

    #use above to query coingecko

    url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart?vs_currency={vs_currency}&days={days}&interval={interval}"
    response = requests.get(url)
    r = response.json()


    df = pd.DataFrame(r['prices'], columns = ["date","price"])
    df['date'] = df['date'].astype('int').astype("datetime64[ms]")
    df['price'] = round(df['price'].astype(float),2)
    df['date'] = df['date'].map(lambda x: x.date())
    df['date'] = df['date'].astype(str)
    print(df.head())

    #add desposit amounts at the correct frequency
    df['deposits'] = 0.0
    df['coin_owned'] = 0.0
    df['avg_portfolio'] = 0.0

    for i in df.index:
        if i == 0:
            df['deposits'][i] = dep_amount
            df['coin_owned'][i] = dep_amount/df['price'][i]
        elif i % frequency_days == 0:
            df['deposits'][i] = dep_amount
            df['coin_owned'][i] = dep_amount/df['price'][i] +df['coin_owned'][i-1]
        else:
            df['coin_owned'][i] = df['coin_owned'][i-1]

        df['avg_portfolio'][i] = round(df['coin_owned'][i]*df['price'][i],2)

    #now create values based on whether the saver invested all money on day 1

    total_investment = sum(df['deposits'])
    df['single_buy_coin']=0.0
    df['single_buy_portfolio']=0.0

    for i in df.index:
        if i ==0:
            df['single_buy_coin'][i] = total_investment/df['price'][i]
            df['single_buy_portfolio'][i] = total_investment
        else:
            df['single_buy_coin'][i] = df['single_buy_coin'][i-1]
            df['single_buy_portfolio'][i] = df['single_buy_coin'][i]*df['price'][i]
    


    df =df.set_index('date')

    dict = df.to_dict()

    return(dict)



app = flask.Flask(__name__)
#app.config["DEBUG"] = True


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