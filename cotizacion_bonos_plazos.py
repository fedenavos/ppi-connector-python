import os
from datetime import datetime
from dotenv import load_dotenv

import pandas as pd
from ppi_client.ppi import PPI
import yfinance as yf

# Load environment variables
load_dotenv()
public_key = os.getenv("PUBLIC_API_KEY")
private_key = os.getenv("PRIVATE_API_KEY")

# Initialize PPI client
ppi = PPI(sandbox=False)
ppi.account.login_api(public_key, private_key)

# Initialize quote dictionary
bono = "AL30"
instrument_to_compare = "BTC-USD"


# Obtener historico de precios en CI, 24hs y 48hs
def obtener_precios():
    precios_48hs = ppi.marketdata.search(
        bono, "Bonos", "A-48HS", datetime(2024, 1, 1), datetime(2024, 5, 23)
    )

    df = pd.DataFrame(
        precios_48hs,
    )

    return df


def get_btc_price():
    # traer precios desde principio de año
    data = yf.download(instrument_to_compare, start="2024-01-01", end="2024-04-23")
    df = pd.DataFrame(data)
    return df


# Actualizar cotizaciones
df = obtener_precios()

# Obtener cotizacion de instrumento a comparar
df_btc = get_btc_price()

print(df)

# Renombrar las columnas para que coincidan
df = df.rename(columns={"date": "Date", "price": "Close AL30"})
df_btc = df_btc.rename(columns={"Close": "Close BTC-USD"})

# Convertir las columnas de fecha a tipo datetime
df["Date"] = pd.to_datetime(df["Date"])
df_btc["Date"] = pd.to_datetime(df_btc.index)

# Localizar la zona horaria (suponiendo UTC-03:00 para ambos)
# df["Date"] = df["Date"].dt.tz_localize('UTC')
df_btc["Date"] = df_btc["Date"].dt.tz_localize('UTC')

# Eliminar la información de la zona horaria
df["Date"] = df["Date"].dt.tz_convert(None)
df_btc["Date"] = df_btc["Date"].dt.tz_convert(None)

# Establecer la columna Date como índice
df.set_index("Date", inplace=True)
df_btc.set_index("Date", inplace=True)

# Unir los dos DataFrames por la columna Date
merged_df = pd.merge(df, df_btc, on="Date")

merged_df.to_csv("merged_df.csv")

# Calcular la correlación entre los precios
correlation = merged_df[["Close AL30", "Close BTC-USD"]].corr()
print(merged_df)

print(correlation)
