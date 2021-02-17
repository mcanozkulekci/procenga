from sklearn.preprocessing import MinMaxScaler
from keras.models import model_from_json
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

sc = MinMaxScaler()
+
json_file = open('model_1h.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("model_1h.h5")
print("Loaded model from disk")


def model_compiling(loaded_model):
    loaded_model.compile(optimizer="adam", loss="mse")
    return loaded_model


def fitting_operation():
    new_df = pd.read_csv('Binance_BTCUSDT_1h.csv')
    df = new_df.drop(['unix', 'date', 'symbol', 'open', 'high', 'low', 'Volume BTC', 'Volume USDT', 'tradecount'], axis=1)
    df = sc.fit_transform(df)

"""
while 1:
    usr_input = float(input("Enter current BTC price for future Price :"))
    scaled_price = sc.transform([[usr_input]])

    predicted_price = loaded_model.predict(scaled_price)
    predicted_price_show=float(predicted_price)
    print("\nOur Guess for 1h Later :{} !!!!\n".format(predicted_price_show))

    if predicted_price>usr_input:
        print("BUY!!\n")
    elif predicted_price<usr_input:
        print("SELL!!\n")"""