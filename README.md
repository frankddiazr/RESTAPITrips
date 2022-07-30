# REST API Using Django, Postgessql and contanized with Docker

Hey everyone!
My name is Frank and I would like to share with you this small proyect created using Django rest Framework (DRF) and contanizaed with Docker, this API will load the data from a csv file sent via HTTP, doing some small transformation with Pandas and store it in Postgres Data base. 


# Deployments
To deploy this API just need to have installed Docker which can be downloaded from [here](https://www.docker.com/products/docker-desktop/), and postman to send the requests to the API, can be downloaded from [here](https://www.postman.com/).
Once installed the applications required, just needed to fork this repository to your local machine and from the folder just downloaded execute the below comands using comand lines tool of your preference :

|           Command                          |Explanation                         |
|----------------|-------------------------------|
|`docker-compose up -d`|Will create the image in docker based on Dockerfiles and docker-compose.yml in background mode          |
|`docker-compose exec apitrips python ./jobsity/manage.py makemigrations`          |Will identify what should be migrated            |
|`docker-compose exec apitrips python ./jobsity/manage.py migrate`          |Will execute the migration based on previous point|


## Trying the API

Once last steps are done, just need to open Postman and send the request to the API! :D

|          URLs                         |Description     |   Parameters                    |
|-------------|----------------------------|-----------------------|
|`http://127.0.0.1:8080/trips/insert`|Allow you to send the file to be loaded, please note tha the key is "file" lowercase.          | Key=file Value=file, this is a POST method and the file can be sent through Postman -> Body-->form-data|
|`http://127.0.0.1:8080/trips/allTrips`|Will return all trips inserted in the DB           | No parameters |
|`http://127.0.0.1:8000/trips/queryByCoordinates/10.00001215152/53.50` |will return a json file format with the weekly average number of trips by region and the coordinates given, noted that this method will return the average which is a float and the number of week in the year. | **longitud(Float)**: This this the Longitud of the coordinates, please be aware that must be in format *99.99999999999*. **latitud(Float)**: This this the Latitud of the coordinates, please be aware that must be in format *99.99999999999+* |
|`http://127.0.0.1:8080/trips/queryByRegion/Hamburg`|will return a json file format with the weekly average number of trips by region, noted that this method will return the average which is a float and the number of week in the year.|**region(Char)**:Name of the region|
