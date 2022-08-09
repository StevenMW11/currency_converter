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

api_key = 'zfzFLkorymExtxaTPo6F' #CREATE THIS ENV VARIABLE FOR USER INPUT

usd_codes = pd.read_excel("conversion_codes_usd.xlsx")
eur_codes = pd.read_excel("conversion_codes_eur.xlsx")
usd_codes_dict = usd_codes.to_dict()
eur_codes_dict = eur_codes.to_dict()

valid_currencies_usd = list(usd_codes_dict['Currency_Code'].values())
valid_currencies_eur = list(eur_codes_dict['Currency_Code'].values())

def currency_check(code):
    if (code in valid_currencies_usd) or (code in valid_currencies_eur):
        True
    else:
        False

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
    viz = viz.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.')
    return viz

def main():
    # DETERMINE YOUR CURRENCIES TO CONVERT (USER INPUT)
    start_currency = input("Which Currency Would You Like To Convert? (USD or EUR) ").upper()

    # STARTING CURRENCY MUST BE USD OR EUR
    if (start_currency == "USD") or (start_currency == "EUR"):
        end_currency = input("Please Input Your Desired Currency To Convert (AUD, CAD, CNY ...): ").upper()
        # VALIDATE THE ENDING CURRENCY USING OUR CURRENCY CHECK FUNCTION
        currency_check(end_currency)
        if True and (start_currency != end_currency): 
            print(f"You Want To Convert {start_currency} to {end_currency}")
            amount_to_convert = float(input("How Much Do You Want To Convert? "))
            conversion_df_creation(start_currency, end_currency)
            exchange_rates_df = conversion_df_creation(start_currency,end_currency)
            latest_exchange_rate = float(exchange_rates_df["Value"][0])
            conversion_amount = amount_to_convert * latest_exchange_rate
            print (f"{amount_to_convert} {start_currency} is equal to {conversion_amount} {end_currency} at the conversion rate of {latest_exchange_rate}")
            viz = dashboard(exchange_rates_df,start_currency,end_currency)
            viz.show()
        else:
            print("You Chose an Invalid Currency to Convert, Please Run Again.")
    else:
        print ("You Chose an Invalid Currency to Convert, Please Run Again.")

if __name__ == "__main__":
    main()