import os
from datetime import datetime

import matplotlib.pyplot as plt
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


strikes = [
    2955.90,
    3105.90,
    3255.90,
    3405.90,
    3555.90,
    3705.90,
    3855.90,
    4005.90,
    4155.90,
    4355.90,
    4555.90,
    4755.90,
    4955.90,
    5155.90,
    5355.90,
]


def format_df(data):
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    return df


def get_opciones_data(strikes, ppi):
    results = []
    for strike in strikes:
        data = ppi.marketdata.search(
            "GFGC" + str(int(strike * 10)) + "J",
            "OPCIONES",
            "A-24HS",
            datetime(2024, 1, 1),
            datetime.now(),
        )
        df = format_df(data)
        results.append(df)
    return results


opciones_data = get_opciones_data(strikes, ppi)
print(opciones_data[0].head())

for i, df in enumerate(opciones_data):
    print(df.head())
    print(df.tail())
    # plt.plot(df["close"], label=str(strikes[i]))
