# JuniorCaseAppTweak

## Requirements
- Flask : 3.0.2
- Pymeos latest version
- MobilityDB : https://github.com/MobilityDB/MobilityDB


## Implementation
There are two main parts in the code :
  - The backend code of the API
  - The databse setup

The api was developped using the python library flask, this allowed me create the API  and her two  endpoint for both locations in the databse and query the data stored in the database based on the user request for the second endpoint.

The database is composed of two  simple tables and a function that allow me thanks to MobilityDb to  get the data for the desired date range by the user


## Use case
### Endpoints
Here is an exmaple of usage of both endpoints.
First  of all to add a location we can use the following url : http://127.0.0.1:5000/addLocation?lon=86&lat=15&slug=new_york
If we use the terminal we get the following result 
![image](https://github.com/wbelgada/JuniorCaseAppTweak/assets/33086974/ce97f664-80df-45b9-a7ce-b0d8bfdc1c69)

But if there is already an existing entry  we get the following response
![image](https://github.com/wbelgada/JuniorCaseAppTweak/assets/33086974/2998cecb-2ac2-4b5c-87d6-fd2e677a3c94)


About the second endpoint, we use an url of the following type : hhtp://127.0.0.1:5000/getTemperatures?slug=blabli&Start_date=2018-02-01&End_date=2018-02-03
if there is data available for the resuqted time range we only send data for the days for which we have some data sotred in the databse:
![image](https://github.com/wbelgada/JuniorCaseAppTweak/assets/33086974/88e792a1-18e6-461e-98a9-df66062f5844)



if there is no data available for the requested time range we get the following result :
![image](https://github.com/wbelgada/JuniorCaseAppTweak/assets/33086974/85ca810c-f2e9-42ff-89af-cac04f14a4b0)

### Bonus
For the bonus I've implmented a simply script that every 3 days will get all the slug from ethe database wiith the cooridantes and start a serie of API request to the 7timer! API to get all the data we need to update the historical trak of temperature of all the locations already present in the database. The scipt that do that is in the dataCollector.py file.



