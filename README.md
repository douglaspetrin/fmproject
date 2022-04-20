[![CircleCI](https://circleci.com/gh/douglaspetrin/fmproject/tree/main.svg?style=svg)](https://circleci.com/gh/douglaspetrin/fmproject/tree/main)
## FMApi

FMApi is a REST API developed in Flask. Its goal is to return the first five items from https://jsonplaceholder.typicode.com/todos.

### Getting started
 To clone repository, build and run containers:

    git clone https://github.com/douglaspetrin/fmproject.git  
    docker-compose build
    docker-compose up

After running commands above it will build and run two images `fmproject_web` and `mysql:5.7`.

That's all! You are good to go and test the application! 

#### The application flow is:  
    1) register an user -->  http://127.0.0.1:5000/register
    2) login with email and password created in step 1 -->  http://127.0.0.1:5000/login  
    3) get todo list by sending access_token received in step 2 into headers -->  http://127.0.0.1:5000/

### cURL commands
###### - register user:
    curl --location --request POST 'http://localhost:5000/register' --header 'Content-Type: application/json' --data-raw '{"name": "maria", "email": "maria@maria.com", "password": "maria123"}'

###### - login:
    curl --location --request POST 'http://localhost:5000/login' --header 'Content-Type: application/json' --data-raw '{"email": "maria@maria.com", "password": "maria123"}'

###### - get todo list: 
    curl --location --request GET 'http://localhost:5000/' --header 'Authorization: Bearer <access_token>'

###### - get todo list (only id and title parameters): 
    curl --location --request POST 'http://localhost:5000/' --header 'Authorization: Bearer <access_token>' --header 'Content-Type: application/json' --data-raw '{"only_id_title": 1}'

### Testing
**make sure to execute `docker-compose build` and `docker-compose up` before running tests.
- Get docker container id: `docker ps`
- Run test with pytest: `docker exec -it <containerId> pytest --cov=fmapi tests/`

### Settings:

- To stop logging data into a file set `LOG_TO_FILE: 0` in `docker-compose.yml`.
- To set new values to environment variables such as `AUTH_TOKEN_EXPIRES_IN` or `FMAPI_SECRET_KEY` go to `docker-compose.yml`.  

**don't forget to update tests if you change any variable value.

### Accessing MySQL from outside docker container

`mysql -h localhost -P 3306 --protocol=tcp -u root -p`  
or `mysql -h 127.0.0.1 -P 3306 -u root -p`
