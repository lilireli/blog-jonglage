# coding: utf-8

import json
import glob
import datetime

from flask import Flask, Response, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from blogapp.models import Category, Article

# Information de connexion
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask('__app__')
#app.secret_key = 'test'

NB_ARTICLES_BY_PAGE = 20

@app.route('/')
def index():
    return 'Hello'

# Renvoie la page HTML de la catégorie
@app.route('/categories/<category>')
def get_category(category):
    # Récupérer les informations concernant la catégorie
    query = session.query(Category.name).filter_by(name=category)
    categories = query.all()
    # Vérifier que la catégorie existe
    if len(categories) == 1:
    # Renvoyer les informations ou une erreur
        return category
    else:
        return 'error'

@app.route('/articles/<category>/list_articles')

@app.route('/articles/list_articles/<page>')

@app.route('/articles/<article>')
def get_article(article):
    # Récupérer les informations concernant l'article
    articles = glob.glob('articles/{article}.json'.format(article=article))
    if articles:
        with open(articles[0]) as input:
            article_dict = json.load(input)
        return Response(str(article_dict), mimetype='json')
    else:
        return 'error'
    # Renvoyer les informations ou une erreur

@app.route('/articles/creation', methods=["GET", "POST"])
def create_article():
    if request.method == "POST" and form.validate():
        now = datetime.datetime.now()
        article = Article(
            name=form.name.data, author=form.author.data,
            content=form.content.data, category_name=form.category.data,
            creation_date=now, last_modification_date=now,
            url=form.name.data)
        session.add(article)
        session.commit()
        return Response("Article enregistré")

if __name__ == '__main__':
    app.run(debug=True)
