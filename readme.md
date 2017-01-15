This project is the creation of a blog onto the juggling. It is in python 3.

# Installation

* Install virtualenv, libffi-dev, libmysqlclient-dev and python-dev
* Create a virtual environment into the application: `virtualenv venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install the necessaries libraries : `pip install -r requirements.txt`
* Verify that your locale (fr_FR.utf8 for french) is installed with `locale -a`
* Create a folder 'instance' at the root. Into it, create a file 'config.py'. Insert the following lines to the config.py file which contains your secret configuration (the password into the variable DB_PASSWORD, and a token in the variable TOKEN):
```
DB_PASSWORD = "password_of_your_database"
TOKEN = "token_of_your_choice"
```
* In the folder 'config', you can find several config file. If you want set your own config, copy one of the config file and replace the parameters by your own.
* Create a file start.sh, which is used to launch the server. Into it insert:
```
export APP_CONFIG_FILE=/absolute/path/to/your/config
venv/bin/python blogapp/views.py
```
The 'APP_CONFIG_FILE=/absolute/path/to/your/config' path is one of the file contained into the config folder (dev_pierrick.py by example).
The second line is used to launch your executable. In dev, `venv/bin/python blogapp/views.py`is suitable.
You have next to set file excutable with a `chmod +x start.sh`

# Installing the database

* Install MariaDB
* Create a database 'jonglage' into MariaDB `CREATE DATABASE jonglage;`
* Create an user with the password defined in your secret configuration `CREATE USER name IDENTIFIED BY 'password';`
* Allow the new user to access to the database `GRANT ALL PRIVILEGES ON jonglage.* TO 'name';`

These steps are uniquely needed if you want to launch the unit test!
* Create a database 'test' into MariaDB if you want to run the test `CREATE DATABASE test;`
* Create an user test without password `CREATE USER test`
* Allow the user test to access to the database test `GRANT ALL PRIVILEGES ON test.* TO 'test';`

# Test the application

* I use py.test to launch my unit tests. There are all in the test folder. You can launch the unit tests with `py.test tests`

# Server launch

Just launch `./start.sh`

To initialize the database make a request on 'localhost:5000/initialize' to initialize the database (use it in dev only). It should ask for your token, which username you have defined in 'config.py' and no password.

It can be launched with swagger (see below)

# Authentication

An authentication with token is provided. The token must be written in the private config file (see below). When you request a page with the authentication, a user/password is asked to you. Just provide the token in the user field.

# API consultation

Consult the page /swagger/index.html

# Launch in prod

You can use the WSGI server you want. Just pass the command to launch it in start.sh. Personnaly, I use chaussette + circus + nginx.

# Docker

I use docker to put the server in prod. You can see my use here: https://github.com/bwatt-fr/server
