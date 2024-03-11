from flask import Flask,request
import requests
import psycopg2 as pg2
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
from urllib.parse import quote, unquote

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

    # Now you can execute SQL queries using the cursor

    # Example: Fetch and print the PostgreSQL version
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("PostgreSQL version:", db_version)

except (Exception, pg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)

app = Flask(__name__)

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




@app.route("/cheminGet")
def getTemp():

    slug = request.args.get('slug')
    select_query = """
                SELECT lon,lat 
                FROM locations
                WHERE slug = %s """

    cursor.execute(select_query, (slug,))

    result = cursor.fetchone()
    if result:
        api_url = f"https://www.7timer.info/bin/astro.php?lon={result[0]}&lat={result[1]}" \
                  f"&ac=0&unit=metric&output=json&tzshift=0"
        try:
            # Make a GET request to the API endpoint
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse and use the response data (in JSON format)
                data = response.json()
                print("API response:", data)
                return data
            else:
                # Print an error message for unsuccessful requests
                print(f"Error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            print("Error during API request:", e)
    else:
        return 'There is no location stored in the databse for the given slug', 500