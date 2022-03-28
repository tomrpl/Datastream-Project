
from calendar import c
import time
import json
import pandas as pd
import numpy as np
import river
import sys
from sklearn.metrics import mean_absolute_percentage_error

from kafka import KafkaConsumer


if __name__ == '__main__':

    name = sys.argv[1]

    topic_name = "binance_topic"
    consumer = KafkaConsumer(topic_name, bootstrap_servers="localhost:9092")

    model = (
        river.preprocessing.StandardScaler() |
        river.tree.HoeffdingTreeRegressor(
            grace_period=200,
            leaf_prediction='adaptive',
            model_selector_decay=0.9
            )
        )
    metric_mae = river.metrics.MAE()
    metric_mape = river.metrics.SMAPE()


    df_results = pd.DataFrame()
    mape = 0

    #name = 'long_test_v2'

    for message in consumer:
        res = json.loads(message.value.decode('utf-8'))
        columns = ['open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'n_trades',
        'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df = pd.DataFrame(res, columns=columns)

        for col in columns:
            df[col] = df[col].astype(float)

        final_row = df.iloc[-1]

        features = []
        for t in [3, 5, 10]:
            open_moy = df.iloc[-t:-1].open.mean()
            open_std = df.iloc[-t:-1].open.std()
            n_trades_sum = df.iloc[-t:-1].n_trades.sum()
            delta = df.iloc[-t].close - df.iloc[-2].close
            feats = np.array([open_moy, open_std, n_trades_sum, delta])
            features.append(feats)
        features = np.array(features).flatten()

        times = ['1m', '3m', '10m']
        col_x = [[f'moy_{t}', f'std_{t}', f'n_trades_sum_{t}', f'delta_{t}'] for t in times]
        col_x = np.array(col_x).flatten()
        x = {col_x[i] : features[i] for i in range(len(features))}
        
        y = final_row.close
        y_pred = model.predict_one(x)

        timestamp = final_row.open_time
        date = time.strftime('%A, %Y-%m-%d %H:%M:%S', time.localtime(timestamp/1000))
        print(f'Prevision at {date}')
        print(f'Predicted value : {y_pred:.2f}')
        print(f'Real value : {y}')
        mae = np.abs(y-y_pred)
        print(f'MAE : {mae:.2f}')
        if y_pred != 0:
            mape = 100*mean_absolute_percentage_error([y], [y_pred])
            print(f'MAPE : {mape:.2f}%')
        new_mae = metric_mae.update(y, y_pred).get()
        print(f'Current MAE : {new_mae:.2f}')
        new_smape = metric_mape.update(y, y_pred).get()
        print(f'Current SMAPE : {new_smape:.3f}%')

        results = [timestamp, y, y_pred, mae, mape, new_mae, new_smape] + list(features)
        print(results)
        cols_res = ['timestamp', 'y', 'y_pred', 'mae', 'mape', 'new_mae', 'new_smape'] + list(col_x)
        print(cols_res)
        df_tmp = pd.DataFrame([results], columns=cols_res)
        df_results = pd.concat((df_results, df_tmp))

        df_results.to_csv(f'./data/df_results_{name}.csv', sep=';', index=False)

        model = model.learn_one(x, y)   
        print()
        print('----------------------------------------------------------------------')
        print()

    time.sleep(1)