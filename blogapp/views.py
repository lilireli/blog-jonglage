# coding: utf-8

import json
import glob
import datetime
import unicodedata
import locale

from flask import Flask, Response, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Article, Tag

# Information de connexion
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask('__app__', template_folder='blogapp/templates',
            static_folder='blogapp/static')
#app.secret_key = 'test'

locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

NB_ARTICLES_BY_PAGE = 20
DATE_STRING_FORMAT = "%d %b %Y"

@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    data = {"test": "test"}
    print data
    return render_template('general-template.html', data=json.dumps(data),
                           type_js='article')


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
    query = session.query(Article).filter_by(id=article)
    articles = query.all()
    # Renvoyer les informations ou une erreur
    if len(articles) == 1:
        article = articles[0]
        tags = [{"name": t.name} for t in article.tags]
        data = {
            "name": article.name,
            "author": article.author,
            "description": article.description,
            "url": article.id,
            "category": article.category.name,
            "page_type": article.category.name,
            "content": article.content,
            "creation_date": article.creation_date.strftime(DATE_STRING_FORMAT),
            "last_modification_date": article.last_modification_date.strftime(DATE_STRING_FORMAT),
            "tags": tags,
        }
        return render_template('general-template.html', data=json.dumps(data),
                                   type_js='article')
    else:
        return 'error'

@app.route('/articles/creation', methods=["POST"])
def create_article():
    if request.method == "POST":
        now = datetime.datetime.now()
        id_art = request.form['name'].lower()
        nfkd_form = unicodedata.normalize('NFKD', id_art)
        id_art = nfkd_form.encode('ASCII', 'ignore')
        id_art = id_art.replace(' ', '-')
        tags = [Tag(name=t) for t in request.form['tags'].split(',')]
        article = Article(
            name=request.form['name'], author=request.form['author'],
            content=request.form['content'], category_name=request.form['category'],
            creation_date=now, last_modification_date=now,
            description=request.form['description'], id=id_art, tags=tags)
        session.add(article)
        session.commit()
        return Response("Article enregistré")
