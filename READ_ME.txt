1 :

-- Welcome to this Data Stream project --

---------------------------------------------------------------------------------
------------- For Master Datascience, March 2022 --------------------------------
---------------------------------------------------------------------------------
------------- The work is a contribution from : ---------------------------------
------------- Paul Fayard, Jean Pachebat, Tom Reppelin.  ------------------------
---------------------------------------------------------------------------------
---------------------------------------------------------------------------------

2: 

Goal:

The goal of this project is to propose comparison of different prediction model over the evolution of 3 cryptocurrencies:

BTC, Bitcoin through btcusdt,
ETH, Ethereum through ethusdt,
and SOL, Solana, through solusdt.

We retrieved the data from the API of binance.

3

By using Kafka, we are creating a topic, where the code of the producer.py script is sending the needed information.
The consumer.py allows us to retrieve the features, and exectue the model (HoeffdingTreeRegressor).

The Animation.py is the script that create the visualisation of the kafka procedure, with the prediction value of each of the 3 streams vs the real value.

4 

Comparison:
By implement a SNARIMAX model of forecasting using time series with the river library, we managed to produce some comparision between our model.

