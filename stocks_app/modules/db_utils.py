#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author:         Durga Prasad Sadhanala
Date Created:   08/20/2022
Functionality:  Utility class/module that helps simplify the database creation and management
"""
import sqlite3

class DBUtils:
    def create_db(self, file_path):
        # create empty database
        self.connection = sqlite3.connect(file_path)
        # establish connection to the DB
        self.cursor = self.connection.cursor()
        print(f"Database created successfully at {file_path}")

        return self.connection, self.cursor

    def create_table(self, table_name, query):
        try:
            isTableExist = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'").fetchall()
            if isTableExist == []:
                self.cursor.execute(f"CREATE TABLE {table_name} {query}")
                print(f"{table_name} table created successfully")
        except OSError as error:
            print(f"Error: '{error}'")

    def add_to_table(self, table_name, query, values):
        try:
            self.cursor.execute(f"INSERT or REPLACE INTO {table_name} {query}", values)
            self.connection.commit()
        except OSError as error:
            print(f"Error: '{error}'")

    def fetchDataFromDB(self, query):
        try:
            self.cursor.execute(query)
            # fetch all rows and convert tuple -> array
            return [list(row) for row in self.cursor.fetchall()]
        except OSError as error:
            print(f"Error: '{error}'")
