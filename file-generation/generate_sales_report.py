#!/usr/bin/env python3

import json
import locale
import sys
import os
import emails
import reports

def load_data(filename):
    """Loads the contents of filename as a JSON file."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def format_car(car):
    """Given a car dictionary, returns a nicely formatted name."""
    return "{} {} ({})".format(
        car["car_make"], car["car_model"], car["car_year"])

def process_data(data):
    """Analyzes the data, looking for maximums.

    Returns a list of lines that summarize the information.
    """
    locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
    max_revenue = {"revenue": 0}
    max_sales = {"total_sales": 0}
    popular_years = {}

    for item in data:
        # Calculate the revenue generated by this model (price * total_sales)
        #We need to convert the price from "$1234.56" to 1234.56
        item_price = locale.atof(item["price"].strip("$"))
        item_sales = item["total_sales"]
        item_revenue = item_sales * item_price
        item_year = item["car"]["car_year"]

        if item_revenue > max_revenue["revenue"]:
            item["revenue"] = item_revenue
            max_revenue = item
            
        # Find max sales
        if item_sales > max_sales["total_sales"]:
            max_sales = item

        # Find most popular car_year
        if not item_year in popular_years:
            popular_years[item_year] = 0

        popular_years[item_year] += item_sales

    max_year = max(popular_years, key=popular_years.get)

    summary = [
        "The {} generated the most revenue: ${}".format(
            format_car(max_revenue["car"]), max_revenue["revenue"]),
        "The {} had the most sales: {}".format(
            format_car(max_sales["car"]), max_sales["total_sales"]),
        "The most popular year was {} with {} sales.".format(
            max_year, popular_years[max_year] 
        )
    ]

    return summary

def cars_dict_to_table(car_data):
    """Turns the data in car_data into a list of lists."""
    table_data = [["ID", "Car", "Price", "Total Sales"]]
    for item in car_data:
        table_data.append([item["id"], format_car(item["car"]), item["price"], item["total_sales"]])
    return table_data

def main(argv):
    """Process the JSON data and generate a full report out of it."""
    data = load_data("car_sales.json")
    summary = process_data(data)
    print(summary)

    # Generate pdf report
    report_path = "/tmp/cars.pdf"
    cars_table = cars_dict_to_table(data)
    reports.generate(report_path, "Vehicle Sales Report", "<br/>".join(summary), cars_table)

    # Send pdf as email attachment
    sender = "automation@example.com"
    receiver = "{}@example.com".format(os.environ.get('USER'))
    subject = "Sales summary for last month"
    body = "\n".join(summary)
    email = emails.generate(sender, receiver, subject, body, report_path)
    emails.send(email, argv[1])
