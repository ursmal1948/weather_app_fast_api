<div align="center">
  <img src="weather_icon.svg" alt="Weather Icon" width="100" />  
  <h1>Weather App</h1>
</div>

### Simple weather application that allows user to check the weather for any location, either by  providing the city or geographical coordinates. Users can choose to fetch live weather data from an external API or create their own custom weather entries, which can be saved to a database for later retrieval.

## Technologies used in the project:
- FastApi - for web layer, providing modern and efficient framework for building APIs. 
- Docker - for containerization of app and services (mysql + redis)
- Redis - used for caching data from external api, allowing for faster access and reduced api call frequency. 
- MySQL - serves as database layer for persistent data storage.

  ## Setup and Commands
- To build and run project in detached mode, run:
```
docker-compose up -d --build
```
It will build necessary images and start the containers, allowing developer to use terminal for other task.

To see the logs of containers, run:
```
docker-compose logs -f
```
Above command is very useful in development, because it provides inforamtion about application performance and any potential issues. 

To stop and remove all the containers, run:
```
docker-compose down
```

To view the interactive API documentation provided by Swagger UI, run application and navigate to the following URL in browser:
```
http://localhost:8000/docs
```

## Migrations
I have used alembic to simplify creation of tables and separate its logic from the logic of managing and manipulating data in database. 
### 
Command for applying migration in container of my app (in app package):
```
alembic upgrade head
```
It creates city and weather tables, making the database functional and ready for programmer to work with the app.

## Example API Request
Brief overview how to interact with the API endpoints:
##
Creating Custom Weather Entry:
- Endpoint: POST /api/internal/weather
- Request Body:
```
{
    "city_name": "Prague",
    "description": "overcast clouds",
    "temperature": 7.22,
    "sunrise": 1730526854,
    "sunset": 1730561846
}
```

Workflow for Creating Custom Weather Data:
1. The user creates custom weather data for a specific location, following a structure presented above.
2. The user sends a POST request to store this entry in the database.
3. If the specified city does not already exist in the database, it is added along with the weather details.
4. Response with status code 201:
```
{
    "id": 4,
    "city_id": 4,
    "description": "overcast clouds",
    "temperature": 7.22,
    "sunrise": "05:54:14",
    "sunset": "15:37:26"
}
```






