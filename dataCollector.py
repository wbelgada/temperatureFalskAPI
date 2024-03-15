import schedule
import time
import psycopg2 as pg2
import requests
import datetime
from psycopg2 import errors

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

def my_function(year,month,day):
    print("Executing my function...")

    current_date = datetime.datetime(year, month, day)

    next_date1 = current_date + datetime.timedelta(days=1)
    next_date2 = current_date + datetime.timedelta(days=2)

    print(current_date,next_date1,next_date2)

    select_query = """SELECT slug, lon, lat
                    FROM locations"""

    cursor.execute(select_query)

    result = cursor.fetchall()
    print(result)
    if result:
        for line in result:
            print(line)
            print("Requesting for slug :",line[0])
            api_url = f"http://www.7timer.info/bin/api.pl?lon={line[1]}&lat={line[2]}&product=astro&output=json"
            # api_url = f"https://www.7timer.info/bin/astro.php?lon={result[0]}&lat={result[1]}" \
            #          f"&ac=0&unit=metric&output=json&tzshift=0"
            try:
                # Make a GET request to the API endpoint
                response = requests.get(api_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse and use the response data (in JSON format)
                    print("The obtained resposnse is :",response)
                    data = response.json()
                    temps = []
                    for elem in data['dataseries']:
                        temps.append(elem['temp2m'])
                    firstDayMin = min(temps[0:8])
                    firstDayMax = max(temps[0:8])
                    secondDayMin = min(temps[8:16])
                    secondDayMax = max(temps[8:16])
                    thirdDayMin = min(temps[16:])
                    thirdDayMax = max(temps[16:])

                    #Insert the data into the databse
                    secondParam = "'{"+f"{firstDayMin}@{current_date},{secondDayMin}@{next_date1},{thirdDayMin}@{next_date2}"+"}'"
                    thirdParam = "'{"+f"{firstDayMax}@{current_date},{secondDayMax}@{next_date1},{thirdDayMax}@{next_date2}"+"}'"
                    sqlFunctionCall = f"""
                                SELECT insert_or_update_location_temp('{line[0]}'::TEXT,{secondParam}::TEXT,{thirdParam}::TEXT)
                                """
                    print("YOOOO",sqlFunctionCall)

                    cursor.execute(sqlFunctionCall)
                    connection.commit()
                    print("Data inserted successfully.")
                else:
                    # Print an error message for unsuccessful requests
                    print(f"Error: {response.status_code} - {response.text}")

            except requests.RequestException as e:
                print("Error during API request:", e)
    else:
        return 'There is no location stored in the databse for the given slug', 500



schedule.every(3).days.at("00:00").do(my_function,datetime.datetime.now().year,
                    datetime.datetime.now().month,datetime.datetime.now().day)
my_function(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day)
while True:
    schedule.run_pending()
    time.sleep(1)
