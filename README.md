# Welcome

## Prerequisites
* Anaconda 3.7+
* Python 3.8+

## Setup

First, download (clone) to your desktop

Then, in your command line (e.g. Terminal), create a virtural enviroment (you only need to do this the first time):

 ```sh
 conda create -n currency_converter python=3.8
 ``` 

Next, activate the virtural enviroment you just made:

 ```sh
 conda activate currency_converter
 ```

Now navigate to the folder the program download exists in (should be your desktop, if you followed step 1) (if on windows, use \ instead of /):

 ```sh
cd ~/Desktop/currency_converter
 ```

Then install the necessary requirments:
```sh
pip install -r requirements.txt
```

### Enviroment Variables
The developer, after signing the contract, will provide a .env file that includes the NASDAQ API Key. **This .env folder must be copied into the main currency_converter folder.** 

# Operation
To run the program, in your command line, run:
```sh
main.py
```

The program will ask the currency to convert from (EUR or USD), the currency to convert to, and the amount you wish to convert.

The program will then fetch the most current exchange rate from NASDAQ, shows the exchange information, and opens your default web browser showing the historical exchange rate trend.