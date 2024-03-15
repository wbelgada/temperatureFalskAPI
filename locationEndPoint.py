from flask import Flask,request
import requests
import json
from datetime import datetime
import psycopg2 as pg2
from pymeos import *
from pymeos.db.psycopg2 import MobilityDB
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION, INVALID_DATETIME_FORMAT
from urllib.parse import quote, unquote

app = Flask(__name__)

#Initialize the library
pymeos_initialize()

conn = {
    'host': 'localhost',
    'database': 'juniorCaseAppTweak',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432',
}

try:
    # Establish a connection to the database
    connection = pg2.connect(**conn)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

except (Exception, pg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/addLocation")
def hello():
    lon = float(request.args.get('lon'))
    lat = float(request.args.get('lat'))
    slug = request.args.get('slug')

    insert_query = """
            INSERT INTO locations (lon, lat, slug)
            VALUES (%s, %s, %s);
            """
    # Replace the values with your actual data
    data_to_insert = (lon, lat, slug)

    try:
        # Execute the insertion query with the provided data
        cursor.execute(insert_query, data_to_insert)
        # Commit the transaction to persist the changes
        connection.commit()
        print("Data inserted successfully.")
        return 'Your location has been succesfully added to the database', 200

    except errors.lookup(UNIQUE_VIOLATION) as e:
        # Handle the unique key constraint violation error here
        # You can print an error message, log the error, or take other appropriate actions
        print(f"Error: {e}")
        # Optionally, you can roll back the transaction
        connection.rollback()
        return 'There is already an existing entry in the database with the current slug', 500

def transform_forecasts(*forecast_tuples):
    result = []

    # Split the input data into min and max parts
    min_forecasts = [item.split('@') for item in forecast_tuples[0].split(', ')]
    max_forecasts = [item.split('@') for item in forecast_tuples[1].split(', ')]

    # Iterate through min and max forecast data simultaneously
    for min_data, max_data in zip(min_forecasts, max_forecasts):
        date_min = datetime.strptime(min_data[1][:10], '%Y-%m-%d').date()

        # Extract min and max forecast values
        min_forecasted = float(min_data[0])
        max_forecasted = float(max_data[0])

        result.append({
            "date": date_min.strftime('%Y-%m-%d'),
            "min-forecasted": min_forecasted,
            "max-forecasted": max_forecasted
        })

    return json.dumps(result, indent=2)


@app.route("/getTemperatures")
def getTemp():

    slug = request.args.get('slug')
    start_date = str(request.args.get('Start_date'))
    end_date = str(request.args.get('End_date'))
    select_query = f"""
                SELECT attime(min_temperature,span('{start_date}'::timestamptz,'{end_date}'::timestamptz, true, true)),
                    attime(max_temperature,span('{start_date}'::timestamptz,'{end_date}'::timestamptz, true, true)) 
                FROM temp2mstore
                WHERE slug = '{slug}'; """

    try :
        cursor.execute(select_query)

        result = cursor.fetchone()

        print(result)
        if result != (None,None) and result != None:
            result = (result[0][1:-1],result[1][1:-1])
            print(result)
            result = transform_forecasts(*result)
            return result, 200
        else :
            return "There is no data available for time range requested", 500
    except errors.lookup(UNIQUE_VIOLATION) as e:
        # Handle the unique key constraint violation error here
        # You can print an error message, log the error, or take other appropriate actions
        print(f"Error: {e}")
        return 'The datatime format is not correct it should be as follow YYYY-MM-DD', 500


if __name__ == '__main__':
    app.run()
