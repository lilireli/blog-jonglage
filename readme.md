This project is the creation of a blog onto the jugglage.

# Installation

* Install virtualenv, libffi-dev, libmysqlclient-dev and python-dev
* Create a virtual environment into the application: `virtualenv venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install the necessaries libraries : `pip install -r requirements.txt`
* Verify that your locale (fr_FR.utf8 for french) is installed with `locale -a`
* Create a folder named instance at the root. Into it, create a config.py file, which contains your secret configuration (the password into the variable DB_PASSWORD)
* Create a file start.sh, which is used to launch the server. It must contains the line `export APP_CONFIG_FILE=/absolute/path/to/your/config'`
And after this line: `venv/bin/python run.py` You have next to set file excutable with a `chmod +x start.sh`
The config in the path is one of the file contains into the config folder (dev_pierrick.py by example). If you want set your own config, copy one of the config file and replace the parameters by your own.
* Install MariaDB
* Create a database jonglage into MariaDB, and a user with a password
* Into the virtual environment, launch a `python blogapp/models.py`. It shoud create your tables, and pop the categories with these in blogapp/categories.json

# Lancement du serveur

Just launch `./start.sh`

# Consultation de l'API

Consult the page /static/swagger/index.html
