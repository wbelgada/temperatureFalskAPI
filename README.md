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
First  of all  to  add a location we can  use the following url : 

