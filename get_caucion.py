from datetime import datetime
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

# intraday = ppi.marketdata.intraday("PESOS1", "CAUCIONES", "INMEDIATA")
# print(intraday)

# intraday = ppi.marketdata.intraday("GGAL", "Acciones", "A-24HS")
# print(intraday)

intraday = ppi.marketdata.intraday("TXAR/JUN24", "Futuros", "INMEDIATA")
print(intraday)

# data = ppi.marketdata.current("YPFD", "Acciones", "A-48HS")
# print(data["price"])


# caucion = ppi.marketdata.search(
#     "PESOS1", "CAUCIONES", "INMEDIATA", datetime(2024, 1, 1), datetime.now()
# )
# print(caucion)

# tasa_3d = ppi.marketdata.search_instrument("RFX", "", "", "")
# print(tasa_3d)

# tasa_3d = ppi.marketdata.search_instrument("GFGC", "OPCIONES", "BYMA", "OPCIONES")
# for i in tasa_3d:
#     print(i)

# market_data = ppi.marketdata.book("GGAL", "Acciones", "A-48HS")
# print(market_data)
# market_data = ppi.marketdata.book("GGAL/JUN24", "Futuros", "INMEDIATA")
# print(market_data)
# 
# market_data = ppi.marketdata.current("GGAL", "Acciones", "A-48HS")

# data = ppi.marketdata.search(
#     "GFGC38559J", "OPCIONES", "A-48HS", datetime(2024, 1, 1), datetime.now()
# )
# print(data)
