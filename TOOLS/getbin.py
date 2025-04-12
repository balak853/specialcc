import csv
import pycountry

# Global cache dictionary for BINs
BIN_CACHE = {}

# Load BIN data into cache once on startup
def load_bin_cache(csv_file='FILES/bins_all.csv'):
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 7:
                    continue  # skip incomplete rows
                BIN_CACHE[row[0]] = {
                    "country": row[1],
                    "flag": row[2],
                    "brand": row[3],
                    "type": row[4],
                    "level": row[5],
                    "bank": row[6]
                }
    except Exception as e:
        print(f"Error loading BIN cache: {e}")

# Call it once when this file is loaded
load_bin_cache()

# Main function to fetch BIN details from cache
async def get_bin_details(cc):
    fbin = cc[:6]
    bin_info = BIN_CACHE.get(fbin, {})

    if not bin_info:
        return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

    brand = bin_info.get("brand", "N/A").upper()
    card_type = bin_info.get("type", "N/A").upper()
    level = bin_info.get("level", "N/A").upper()
    bank = bin_info.get("bank", "N/A").upper()
    country_code = bin_info.get("country", "N/A").upper()
    flag = bin_info.get("flag", "N/A").upper()
    country_name = "N/A"
    currency = "N/A"

    if country_code != "N/A":
        try:
            country = pycountry.countries.get(alpha_2=country_code)
            if country:
                country_name = country.name
                currency_obj = pycountry.currencies.get(numeric=country.numeric)
                if currency_obj:
                    currency = currency_obj.alpha_3
        except:
            pass

    if country_name == "N/A":
        country_name = bin_info.get("country", "N/A").upper()

    return brand, card_type, level, bank, country_name, flag, currency
