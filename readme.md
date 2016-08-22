Ce projet concerne la création d'un blog sur le jonglage.

# Installation

* Installer virtualenv, libffi-dev et python-dev
* Créer un environnement virtuel dans l'application : `virtualenv venv`
* Activer l'environnement virtuel : `source venv/bin/activate`
* Installer les librairies : `pip install -r requirements.txt`
* Vérifier que fr_FR.utf8 est installé avec `locale -a`

# Lancement du serveur

Après avoir activé l'environnement virtuel, faire `python web.py`

# Consultation de l'API

Aller dans le dossier swagger et lancer un serveur.
Par exemple lancer `python -m SimpleHTTPServer 8000`
