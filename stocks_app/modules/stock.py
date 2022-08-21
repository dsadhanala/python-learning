#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author:         Durga Prasad Sadhanala
Date Created:   08/20/2022
Functionality:  Stock class
"""
from datetime import datetime

class Stock():
    def __init__(self, stock_symbol, number_of_shares):
        self.name = stock_symbol.upper()
        self.number_of_shares = number_of_shares
        self.stock_id = f"{stock_symbol}_{number_of_shares}".lower()

        self.years_list = []
        self.closing_price_list = []
        self.current_value_list = []

        # self.add_to_data_to_lists(date, closing_price)

    def current_value(self, closing_price):
        return round((self.number_of_shares * round(closing_price, 2)), 2)

    def add_to_data_to_lists(self, date, closing_price):
        year_month = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
        self.years_list.append(year_month)
        self.closing_price_list.append(float(closing_price))
        self.current_value_list.append(self.current_value(closing_price))
