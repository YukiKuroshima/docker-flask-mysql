# Requrements
* Docker
* Docker compose
* Git

# Install
1. Make directory that you want to install this base project and go to the directory
```
mkdir myproject
cd myproject
```

2. Clone this repo
```
git clone https://github.com/YukiKuroshima/docker-flask-mysql.git .
```

3. Start up the docker containers
```
docker-compose up
```

4. Create tables and seed some data
```
docker-compose run users-services python manage.py recreate_db
docker-compose run users-services python manage.py seed_db
```

5. Go to your browser and type below
```
localhost/ping
```
You should see `pong`

```
localhost/users
```
You should see the list of users from database


# Commands
Wants to run docker containers in backgroud?
```
docker-compose -d up
```

Made change in Dockerfile or docker-compose.yml?
<br>Let's Re-build and run
```
docker-compose --build up
```

Run default test cases (Testing config, template rendering, and database connection
```
docker-compose run users-services python manage.py test
```


# TODO
* Scriptize useful commands
* SSH?
