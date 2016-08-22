Ce projet concerne la création d'un blog sur le jonglage.

# Installation

* Installer virtualenv, libffi-dev, libmysqlclient-dev et python-dev
* Créer un environnement virtuel dans l'application : `virtualenv venv`
* Activer l'environnement virtuel : `source venv/bin/activate`
* Installer les librairies : `pip install -r requirements.txt`
* Vérifier que fr_FR.utf8 est installé avec `locale -a`

# Lancement du serveur

Après avoir activer l'environnement virtuel, faire `python web.py`
