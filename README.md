# Crypto Dollar Cost Averaging API

Uses coingecko to create a new API that summarises the results of dollar cost averaging a particular crypto currency over time vs a single bulk investment.

This API is hosted on Heroku [here][https://dca-crypto.herokuapp.com/]

## Structure of the Code
The API receives a number of inputs:
* Cryptocurrency
* Fiat Currency
* Investment Start Date
* Deposit Amount
* Frequency of Deposits

The first three are used to query [CoinGecko's API][https://www.coingecko.com/en/api] and return a dataframe of a particular crypto's price from the start date to today.

The dataframe then uses this information to calculate the user's portfolio investment value based on their dollar cost averaging parameters, as well as insights into the performance of a bulk buy taking place on the initial start date for comparison.

The above is wrapped into a flask app and hosted on Heroku.

This was part of a one day hackathon where I built the backend and and my co-hacker build a [front end interface][https://github.com/MintyFresh-2/dca-crypto] that allowed users to interface with it and see graphs of their portfolio over time.


For more detail on the hackathon, and to try out the final interface, please check out my [blog][https://local-optimum.github.io/local-optimum-blog/hackathons/2021/08/02/dollar-cost-avg-hackathon.html] on the subject.