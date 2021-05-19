from keras.models import model_from_json
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

#Model and Weights Loading
sc = MinMaxScaler()
json_file = open('model_1h.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model_1h.h5")
print("Loaded model from disk")

def loading_model_weights():
    pass



def model_compiling(loaded_model):
    loaded_model.compile(optimizer="adam", loss="mse")
    return loaded_model


#Dataframe Manuplation for unnecessary parts.
new_df = pd.read_csv('Binance_BTCUSDT_1h.csv')
df = new_df.drop(['unix', 'date', 'symbol', 'open', 'high', 'low', 'Volume BTC', 'Volume USDT', 'tradecount'], axis=1)
#Fitting the model
df = sc.fit_transform(df)