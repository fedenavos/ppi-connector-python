import os
import json
from datetime import datetime
from dotenv import load_dotenv

from ppi_client.models.instrument import Instrument
from ppi_client.ppi import PPI

# Load environment variables
load_dotenv()
public_key = os.getenv("PUBLIC_API_KEY")
private_key = os.getenv("PRIVATE_API_KEY")

# Initialize PPI client
ppi = PPI(sandbox=False)

# Initialize quote dictionary
cotizaciones = {
    f"{currency}-{bond}": 0
    for currency in ("MEP", "CCL")
    for bond in ("AL30", "AL35", "GD30")
}
cotizaciones.update(
    {
        bond: 0
        for bond in (
            "AL30",
            "AL30C",
            "AL30D",
            "AL35",
            "AL35C",
            "AL35D",
            "GD30",
            "GD30C",
            "GD30D",
        )
    }
)


def actualizar_cotizaciones():
    """Update and display current exchange rates."""
    for currency in ["MEP", "CCL"]:
        for bond in ["AL30", "AL35", "GD30"]:
            if currency == "MEP":
                cotizaciones[f"{currency}-{bond}"] = (
                    cotizaciones[bond] / cotizaciones[f"{bond}D"]
                )
            elif currency == "CCL":
                cotizaciones[f"{currency}-{bond}"] = (
                    cotizaciones[bond] / cotizaciones[f"{bond}C"]
                )

    print("\nCotizacion a las", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    for key, value in cotizaciones.items():
        if "-" in key:
            print(f"Dolar {key} calculado: {value:.3f}")


def onconnect_marketdata():
    """Actions upon connecting to market data."""
    print("\nConnected to realtime market data\nSearching Current MarketData")
    for bond in [
        "AL30",
        "AL30C",
        "AL30D",
        "AL35",
        "AL35C",
        "AL35D",
        "GD30",
        "GD30C",
        "GD30D",
    ]:
        response = ppi.marketdata.current(bond, "BONOS", "INMEDIATA")
        cotizaciones[bond] = response["price"]

    actualizar_cotizaciones()
    for bond in [
        "AL30",
        "AL30C",
        "AL30D",
        "AL35",
        "AL35C",
        "AL35D",
        "GD30",
        "GD30C",
        "GD30D",
    ]:
        ppi.realtime.subscribe_to_element(Instrument(bond, "BONOS", "INMEDIATA"))


def ondisconnect_marketdata():
    """Actions upon disconnecting from market data."""
    print("\nDisconnected from realtime market data")


def onmarketdata(data):
    """Handle incoming market data updates."""
    msg = json.loads(data)
    if msg.get("Trade"):
        cotizaciones[msg["Ticker"]] = msg["Price"]
        actualizar_cotizaciones()


def main():
    try:
        ppi.account.login_api(public_key, private_key)
        ppi.realtime.connect_to_market_data(
            onconnect_marketdata, ondisconnect_marketdata, onmarketdata
        )
        ppi.realtime.start_connections()
    except Exception as ex:
        print("An error occurred:", ex)


if __name__ == "__main__":
    main()
