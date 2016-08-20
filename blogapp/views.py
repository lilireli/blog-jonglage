# coding: utf-8

import json
import glob
import datetime

from flask import Flask, Response, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Article

# Information de connexion
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask('__app__', template_folder='blogapp/templates',
            static_folder='blogapp/static')
#app.secret_key = 'test'

NB_ARTICLES_BY_PAGE = 20

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    return render_template('index.html')


# Renvoie la catégorie avec tous ses articles
@app.route('/categories/<category>')
def get_category(category):
    # Récupérer les informations concernant la catégorie
    query = session.query(Category.name).filter_by(name=category)
    categories = query.all()
    # Vérifier que la catégorie existe
    if len(categories) == 1:
    # Renvoyer les informations ou une erreur
        return render_template(category + '.html')
    else:
        return 'error'


@app.route('/articles/<article>')
def get_article(article):
    # Récupérer les informations concernant l'article
    query = session.query(Article.name).filter_by(id=article)
    articles = query.all()
    # Renvoyer les informations ou une erreur
    if len(articles) == 1:
        return 'Go'
    else:
        return 'error'

@app.route('/articles/creation', methods=["GET", "POST"])
def create_article():
    if request.method == "POST" and form.validate():
        now = datetime.datetime.now()
        id = lower(form.name.data)
        (id.replace(' ', '-').replace('é', 'e').replace('è', 'e')
           .replace('à', 'a').replace('ê', 'e').replace('ê', 'e'))
        article = Article(
            name=form.name.data, author=form.author.data,
            content=form.content.data, category_name=form.category.data,
            creation_date=now, last_modification_date=now,
            id=id)
        session.add(article)
        session.commit()
        return Response("Article enregistré")
