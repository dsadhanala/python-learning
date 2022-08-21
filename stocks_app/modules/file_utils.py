#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author:         Durga Prasad Sadhanala
Date Created:   08/20/2022
Functionality:  File utils to help read data from JSON and CSV files
"""
from pandas import read_csv
import sys

# read from CSV and return rows as lists
def get_CSV(file_path):
    try:
        # import data from the csv file using
        data_from_csv = read_csv(file_path, header = 0, sep =',')
        header_list = data_from_csv.columns

        # sort list based on symbol name
        dat_list = sorted(data_from_csv.values, key= lambda item: item[0])

        # convert list of lists into dictionary
        stocks_dict = {
            name: {
                'number_of_shares': number_of_shares,
                'purchase_date': purchase_date
            }  for name, number_of_shares, purchase_date in dat_list
        }

        return stocks_dict
    except OSError as error:
        sys.exit(f'\n{error}.')
