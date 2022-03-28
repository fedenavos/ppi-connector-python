from ppi_client.models.account_movements import AccountMovements
from ppi_client.ppi import PPI
from ppi_client.models.orders_filter import OrdersFilter
from ppi_client.models.order_budget import OrderBudget
from ppi_client.models.order_confirm import OrderConfirm
from ppi_client.models.disclaimer import Disclaimer
from ppi_client.models.search_instrument import SearchInstrument
from ppi_client.models.search_marketdata import SearchMarketData
from ppi_client.models.search_datemarketdata import SearchDateMarketData
from ppi_client.models.order import Order
from ppi_client.models.instrument import Instrument
from datetime import datetime, timedelta
import asyncio
import json
import traceback

# Change sandbox variable to False to connect to production environment
ppi = PPI(sandbox=False)

#Listado con las cotizaciones que se van a usar
cotizaciones = {
    "MEP-AL30": 0,
    "CCL-AL30": 0,
    "MEP-GD30": 0,
    "CCL-GD30": 0,
    "AL30": 0,
    "AL30C": 0,
    "AL30D": 0,
    "GD30": 0,
    "GD30C": 0,
    "GD30D": 0
}

#Recalcula las cotizaciones y las muestra en pantalla
def calcular_y_mostrar():
    cotizaciones["MEP-AL30"] = cotizaciones["AL30"] / cotizaciones["AL30D"]
    cotizaciones["CCL-AL30"] = cotizaciones["AL30"] / cotizaciones["AL30C"]
    cotizaciones["MEP-GD30"] = cotizaciones["GD30"] / cotizaciones["GD30D"]
    cotizaciones["CCL-GD30"] = cotizaciones["GD30"] / cotizaciones["GD30C"]

    print("\nCotizacion a las %s" % datetime.now())
    print("Dolar MEP calculado con AL30 %.3f" % cotizaciones["MEP-AL30"])
    print("Dolar CCL calculado con AL30 %.3f" % cotizaciones["CCL-AL30"])
    print("Dolar MEP calculado con GD30 %.3f" % cotizaciones["MEP-GD30"])
    print("Dolar CCL calculado con GD30 %.3f" % cotizaciones["CCL-GD30"])


def main():
    try:
        ppi.account.login('<user key>', '<user secret>')

        def onconnect_marketdata():
            try:
                print("\nConnected to realtime market data")

                # Obtengo las ultimas cotizaciones de cada instrumento
                print("\nSearching Current MarketData")
                msg = ppi.marketdata.current(SearchMarketData("AL30", "BONOS", "INMEDIATA"))
                cotizaciones["AL30"] = msg['price']
                msg = ppi.marketdata.current(SearchMarketData("AL30C", "BONOS", "INMEDIATA"))
                cotizaciones["AL30C"] = msg['price']
                msg = ppi.marketdata.current(SearchMarketData("AL30D", "BONOS", "INMEDIATA"))
                cotizaciones["AL30D"] = msg['price']

                msg = ppi.marketdata.current(SearchMarketData("GD30", "BONOS", "INMEDIATA"))
                cotizaciones["GD30"] = msg['price']
                msg = ppi.marketdata.current(SearchMarketData("GD30C", "BONOS", "INMEDIATA"))
                cotizaciones["GD30C"] = msg['price']
                msg = ppi.marketdata.current(SearchMarketData("GD30D", "BONOS", "INMEDIATA"))
                cotizaciones["GD30D"] = msg['price']

                calcular_y_mostrar()

                # Me suscribo a novedades
                ppi.realtime.subscribe_to_element(Instrument("AL30", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL30C", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("AL30D", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30C", "BONOS", "INMEDIATA"))
                ppi.realtime.subscribe_to_element(Instrument("GD30D", "BONOS", "INMEDIATA"))

            except Exception as error:
                traceback.print_exc()

        def ondisconnect_marketdata():
            try:
                print("\nDisconnected from realtime market data")
            except Exception as error:
                traceback.print_exc()

        # Realtime MarketData
        def onmarketdata(data):
            try:
                msg = json.loads(data)

                #Si fue una nueva cotizacion
                if msg["Trade"]:
                    cotizaciones[msg['Ticker']] = msg['Price']

                    calcular_y_mostrar()
            except Exception as error:
                print(datetime.now())
                print("Error en marketdata: %s. Trace:\n" % error)
                traceback.print_exc()

        ppi.realtime.connect_to_market_data(onconnect_marketdata, ondisconnect_marketdata, onmarketdata)

    except Exception as message:
        print(message)


if __name__ == '__main__':
    main()