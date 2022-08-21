#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author:         Durga Prasad Sadhanala
Date Created:   08/20/2022
Functionality:  Portfolio assignment for week10. This covers, reading and writing to a file, saving data to the database, using classes, function, modularization, using external API's and data visualization through charts from the data.
"""
import matplotlib.pyplot as plt
from yfinance import Ticker
from datetime import datetime
import pandas as pd

# local modules
from modules.file_utils import get_CSV
from modules.stock import Stock
from modules.db_utils import DBUtils

# create global variable for database
manage_db = DBUtils()
manage_db.create_db('stocks_data.db')

# Generate stocks data for the first time and save it to DB
# once exist, use it from DB
def generate_stocks_data(stocks_dict):
    stocks_data_dict = {}
    current_date = datetime.now().strftime("%Y-%m-%d")
    interval = '1d'

    for stock_name in stocks_dict:
        date = stocks_dict[stock_name]['purchase_date']
        number_of_shares = stocks_dict[stock_name]['number_of_shares']
        purchase_date = datetime.strptime(date, '%Y-%m-%d').date()

        split_table = f'{stock_name}_split'
        stock_data_from_given_period = None
        stock_split_shares = 1

        # check if data for the specific stock already exist in DB
        # if not, fetch from the API otherwise use it from DB instead
        try:
            stock_data_from_given_period = pd.read_sql_query(f'SELECT * FROM {stock_name}', manage_db.connection)
            print(f'Table exist for {stock_name}!')

            closing_price_list = stock_data_from_given_period['Close'].tolist()
            dates_list = stock_data_from_given_period['Date'].tolist()
            split_table_list = manage_db.fetchDataFromDB(f'SELECT split_stock_number FROM {split_table}')
            stock_split_shares = [item for sub_list in split_table_list for item in sub_list][0]

        except:
            print(f'Table for {stock_name} does not exist! so fetching from the API.')
            # fetch from the API
            stock_data_from_given_period, stock_split_shares = fetch_stock_prices_from_api(
                stock_name,
                purchase_date,
                current_date,
                interval
            )
            closing_price_list = stock_data_from_given_period['Close'].tolist()
            dates_list = stock_data_from_given_period.index

            # create table and add it to DB
            stock_data_from_given_period.to_sql(stock_name, manage_db.connection, if_exists='replace', index=True)

            # add stock split information to the table
            manage_db.create_table(split_table, "(id text PRIMARY KEY, symbol text, split_stock_number integer)")
            manage_db.add_to_table(split_table, "VALUES (?,?,?)", (split_table, stock_name, stock_split_shares))

        # use first closing price from the list
        closing_price = closing_price_list[0]

        # initialize stock
        stocks_data_dict[stock_name] = Stock(stock_name, number_of_shares * stock_split_shares)

        for index, date in enumerate(dates_list):
            stocks_data_dict[stock_name].add_to_data_to_lists(date, closing_price_list[index])

    return stocks_data_dict

# Fetch data from the API
def fetch_stock_prices_from_api(stock_name, purchase_date, current_date, interval):
    ticker = Ticker(stock_name)
    ticker_data = ticker.history(
        start=purchase_date,
        end=current_date,
        interval=interval,
        actions=False
    )

    # check for splits, if not available set to 1
    # can be improved to allow all splits, for the simplification using one first split data
    ticker_split = ticker.splits.tolist()[0] if ticker.splits.tolist() else float(1)

    return ticker_data, ticker_split

def main():
    # read list of stock symbol, purchase date and number of shares
    stocks_dict_from_CSV = get_CSV('data/stocks.csv')

    # process data and generate consumable stocks dictionary
    stocks_dict = generate_stocks_data(stocks_dict_from_CSV)

    # UNCOMMENT: to fetch data from the DB
    # print(pd.read_sql_query('SELECT * FROM GOOG', manage_db.connection))

    # create plots from the data
    for stock in stocks_dict.values():
        plt.plot(stock.years_list, stock.current_value_list, label=stock.name)

    plt.gcf().autofmt_xdate()
    plt.legend()
    plt.tight_layout()
    plt.savefig('stocks_value_plot.png')
    # plt.show()

    # close database connection
    manage_db.connection.close()

if __name__ == '__main__':
    main()
