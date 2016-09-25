This project is the creation of a blog onto the jugglage.

# Installation

* Install virtualenv, libffi-dev, libmysqlclient-dev and python-dev
* Create a virtual environment into the application: `virtualenv venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install the necessaries libraries : `pip install -r requirements.txt`
* Verify that your locale (fr_FR.utf8 for french) is installed with `locale -a`
* Create a folder named instance at the root. Into it, create a config.py file, which contains your secret configuration (the password into the variable DB_PASSWORD, and a token in the variable TOKEN)
* Create a file start.sh, which is used to launch the server. It must contains the line `export APP_CONFIG_FILE=/absolute/path/to/your/config`
And after a line to launch your executable. In dev, you can set this: `venv/bin/python blogapp/views.py`. You have next to set file excutable with a `chmod +x start.sh`
* The config in the path is one of the file contains into the config folder (dev_pierrick.py by example). If you want set your own config, copy one of the config file and replace the parameters by your own.
* Install MariaDB
* Create a database jonglage into MariaDB, and a user with the password define in your secret configuration
* Run the server, and make a request on /initialize to initialize the database (token use). It can be launched with swagger (see below)

# Server launch

Just launch `./start.sh`

# Authentication

An authentication with token is provided. The token must be written in the private config file (see below). When you request a page with the authentication, a user/password is asked to you. Just provide the token in the user field.

# API consultation

Consult the page /swagger/index.html

# Launch in prod

You can use the WSGI server you want. Just pass the command to launch it in start.sh. Personnaly, I use chaussette + circus + nginx.

# Docker

I use docker to put the server in prod. You can see my use here: https://github.com/bwatt-fr/server
