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

# tasa_1d = ppi.marketdata.intraday("PESOS1", "CAUCIONES", "INMEDIATA")
# print(tasa_1d)

# tasa_3d = ppi.marketdata.search_instrument("GGAL", "", "ROFEX", "")
# print(tasa_3d)

# tasa_3d = ppi.marketdata.search_instrument("PESOS", "CAUCIONES", "BYMA", "CAUCIONES")
# for i in tasa_3d:
#     if i["type"] == "CAUCIONES":
#         print(i["ticker"])

# market_data = ppi.marketdata.book("GGAL", "Acciones", "A-48HS")
# print(market_data["offers"][0]["price"])
# market_data = ppi.marketdata.book("GGAL/ABR24", "Futuros", "INMEDIATA")
# print(market_data["offers"][0]["price"])


