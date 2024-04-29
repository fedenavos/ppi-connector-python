import concurrent.futures
import os

import pandas as pd
from dotenv import load_dotenv
from ppi_client.ppi import PPI

# Load environment variables
load_dotenv()
public_key = os.getenv("PUBLIC_API_KEY")
private_key = os.getenv("PRIVATE_API_KEY")

# Initialize PPI client
ppi = PPI(sandbox=False)
ppi.account.login_api(public_key, private_key)

# Cargar los datos
df = pd.read_csv("rfx_index.csv")


# El df tiene 'ticker' y 'ponderacion'
# Por cada ticker, obtener las cotizaciones actuales y calcular el valor del índice
def get_market_data(row):
    ticker = row["ticker"]
    try:
        print(f"Obteniendo cotización para {ticker}")
        market_data = ppi.marketdata.book(ticker, "Acciones", "A-48HS")
        return {
            "ticker": ticker,
            "bid": market_data["bids"][0]["price"],
            "offer": market_data["offers"][0]["price"],
            "index_value": row["ponderacion"] * market_data["offers"][0]["price"],
        }
    except Exception as e:
        print(f"Error al obtener la cotización para {ticker}: {e}")
        return None


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(get_market_data, [row for _, row in df.iterrows()])

for result in results:
    if result is not None:
        df.loc[df["ticker"] == result["ticker"], "bid"] = result["bid"]
        df.loc[df["ticker"] == result["ticker"], "offer"] = result["offer"]
        df.loc[df["ticker"] == result["ticker"], "index_value"] = result["index_value"]


# Calcular el valor del índice
index_value = df["index_value"].sum()
print(f"El valor del índice segun los calculos es: {index_value}")

# Calcular valor real
rfx20_value = ppi.marketdata.book("RFX20/ABR24", "Futuros", "INMEDIATA")["offers"][0][
    "price"
]
print(f"El valor del índice según el mercado es: {rfx20_value}")

df.to_excel("rfx_index_con_cotizaciones.xlsx", index=False)
