# PREPROCESSING (CREATE THE DICTIONARIES OF EXCHANGE RATES)
# USER INPUT FOR START CURRENCY
# USER INPUT FOR END CURRENCY
# USER INPUT FOR AMOUNT TO CONVERT
# VALIDATION OF CORRECT END CURRENCY & NOT 1-1 CONVERSION
# ACCESS NASDAQ FOR CORRECT INFO (DF)
    # DATAFRAME OF HISTORY AND LATEST EXCHANGE RATE
# PRESENT CONVERSION (WITH RATE)

import os
import requests
import plotly.express as px
import pandas as pd
import pandas_datareader.data as web
from datetime import date
from dotenv import load_dotenv

API_KEY = "zfzFLkorymExtxaTPo6F"

load_dotenv()
#api_key = str((os.getenv('API_KEY')))
api_key = "zfzFLkorymExtxaTPo6F"
usd_codes = pd.read_excel("conversion_codes_usd.xlsx")
eur_codes = pd.read_excel("conversion_codes_eur.xlsx")
usd_codes_dict = usd_codes.to_dict()
eur_codes_dict = eur_codes.to_dict()

valid_currencies_usd = list(usd_codes_dict['Currency_Code'].values())
valid_currencies_eur = list(eur_codes_dict['Currency_Code'].values())

def currency_check(start_currency, end_currency):
    if start_currency == "USD":
        if end_currency in valid_currencies_usd:
            return True
        else:
            return False
    else:
        if end_currency in valid_currencies_eur:
            return True
        else:
            return False

# ACCESS THE DATA FROM NASDAQ & SAVE TO PANDAS DATA FRAME
def conversion_df_creation(start_currency, end_currency):
    if start_currency == "USD":
        position = valid_currencies_usd.index(end_currency)
        fred_code = usd_codes_dict["FRED_Code"][position]
        url_usd = f"https://data.nasdaq.com/api/v3/datasets/FRED/{fred_code}.csv?api_key={api_key}"
        conversion_df = pd.read_csv(url_usd)
        return conversion_df
    else:
        position = valid_currencies_eur.index(end_currency)
        ecb_code = eur_codes_dict["ECB_Code"][position]
        url_eur = f"https://data.nasdaq.com/api/v3/datasets/ECB/{ecb_code}.csv?api_key={api_key}"
        conversion_df = pd.read_csv(url_eur)
        return conversion_df

# VISUALIZE EXCHANGE RATE OVER TIME
def dashboard(dataframe, start_currency, end_currency):
    viz = px.line(data_frame=dataframe,x="Date",y="Value",title=f"Daily Exchange Rate ({start_currency} to {end_currency})",labels={"Date":"Date","Value":"Exchange Rate"})
    viz = viz.update_yaxes(nticks=10)
    viz = viz.update_layout(yaxis_tickformat = ',.')
    viz = viz.update_layout(
    # https://stackoverflow.com/questions/61782622/plotly-how-to-add-a-horizontal-scrollbar-to-a-plotly-express-figure
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )
    return viz

def main():
    print("")
    print("Welcome to Your Currency Converter & Dashboard")
    print("")
    # DETERMINE YOUR CURRENCIES TO CONVERT (USER INPUT)
    start_currency = input("Which Currency Would You Like To Convert? (USD or EUR) ").upper()

    # STARTING CURRENCY MUST BE USD OR EUR
    if (start_currency == "USD") or (start_currency == "EUR"):
        end_currency = input("Please Input Your Desired Currency To Convert (AUD, CAD, CNY ...): ").upper()
        # VALIDATE THE ENDING CURRENCY USING OUR CURRENCY CHECK FUNCTION
        if currency_check(start_currency,end_currency): 
            if start_currency != end_currency:
                print(f"You Want To Convert {start_currency} to {end_currency}")
                amount_to_convert = float(input("How Much Do You Want To Convert? "))
                print("Fetching Data...")
                conversion_df_creation(start_currency, end_currency)
                exchange_rates_df = conversion_df_creation(start_currency,end_currency)
                latest_exchange_rate = float(exchange_rates_df["Value"][0])
                conversion_amount = amount_to_convert * latest_exchange_rate
                amount_to_convert_clean = f"{amount_to_convert:,.2f}"
                latest_exchange_rate_clean = f"{latest_exchange_rate:,.2f}"
                conversion_amount_clean = f"{conversion_amount:,.2f}"
                print("")
                print (f"{amount_to_convert_clean} {start_currency} is equal to {conversion_amount_clean} {end_currency} at the conversion rate of {latest_exchange_rate_clean}")
                print("Stay Tuned For Your Dashboard (Historical Exchange Rates)")
                viz = dashboard(exchange_rates_df,start_currency,end_currency)
                viz.show()
            else:
               print(f"You Can't Convert {start_currency} to itself, Please Run Again.") 
        else:
            print(f"{end_currency} Is Not A Valid Currency To Convert To With {start_currency}, Please Run Again.")
    else:
        print (f"{start_currency} Is Not A Valid Currency To Convert, Please Run Again.")

if __name__ == "__main__":
    main()