import os
from dotenv import load_dotenv

from ppi_client.ppi import PPI

# Load environment variables
load_dotenv()
public_key = os.getenv("PUBLIC_API_KEY")
private_key = os.getenv("PRIVATE_API_KEY")

# Get holidays for the year 2020
ppi = PPI(sandbox=False)
ppi.account.login_api(public_key, private_key)

holidays = ppi.configuration.get_holidays(
    start_date="2024-05-01", end_date="2024-12-31"
)

for h in holidays:
    print(h["date"], h["description"])