import os
import json
from datetime import datetime
from dotenv import load_dotenv

import pandas as pd
from ppi_client.models.instrument import Instrument
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


# Obtener historico de precios en CI, 24hs y 48hs
def obtener_precios():
    for bono in bonos:
        precios_ci = ppi.marketdata.search(
            bono, "Bonos", "INMEDIATA", datetime(2024, 4, 1), datetime(2024, 4, 23)
        )
        precios_24hs = ppi.marketdata.search(
            bono, "Bonos", "A-24HS", datetime(2024, 4, 1), datetime(2024, 4, 23)
        )
        precios_48hs = ppi.marketdata.search(
            bono, "Bonos", "A-48HS", datetime(2024, 4, 1), datetime(2024, 4, 23)
        )

        print(f"\nPrecios para el bono {bono}")
        print("CI")
        print(precios_ci)

        df = pd.DataFrame(
            precios_ci,
        )

        print(df)


# Actualizar cotizaciones
obtener_precios()
