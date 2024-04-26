import os
from dotenv import load_dotenv

import pandas as pd
from ppi_client.ppi import PPI

# Load environment variables
load_dotenv()
public_key = os.getenv("PUBLIC_API_KEY")
private_key = os.getenv("PRIVATE_API_KEY")

# Initialize PPI client
ppi = PPI(sandbox=False)
ppi.account.login_api(public_key, private_key)

# Initialize quote dictionary
bonos = ["AL30", "GD30"]
acciones = ["GGAL", "YPFD", "PAMP"]


def obtener_precios(
    instrument, instrument_type, settlements=["INMEDIATA", "A-24HS", "A-48HS"]
):
    dfs = []
    df = pd.DataFrame()
    for settlement in settlements:
        precios = ppi.marketdata.intraday(instrument, instrument_type, settlement)

        df = pd.DataFrame(precios)
        df = df[["date", "price"]]
        df.drop_duplicates(subset="date", keep="last", inplace=True)
        
        # Asegurar que 'date' es tipo datetime y establecer como índice
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        # Rellenar los minutos faltantes usando ffill()
        df = df.asfreq('min').ffill()
        
        dfs.append(df.reset_index())

    # Merge dataframes
    df = pd.merge(
        dfs[0],
        dfs[1],
        on="date",
        how="left",
        suffixes=("", "_24HS"),
    )
    df = pd.merge(
        df,
        dfs[2],
        on="date",
        how="left",
        suffixes=("", "_48HS"),
    )

    return df


# Actualizar cotizaciones
for bono in bonos:
    df = obtener_precios(bono, "Bonos")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(f"outputs/{bono}.xlsx", index=False)

for accion in acciones:
    df = obtener_precios(accion, "Acciones")
    df["date"] = df["date"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(f"outputs/{accion}.xlsx", index=False)
