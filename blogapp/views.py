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
    return render_template('general-template.html', data=json.dumps(data),
                           type_js='home')


# Renvoie la catégorie avec tous ses articles
@app.route('/categories/<category>')
def get_category(category):
    # Récupérer les informations concernant la catégorie
    query_cat = session.query(Category).filter_by(id=category)
    categories = query_cat.all()

    # Récupération des beginners links
    query_beginner = (session.query(Article.name, Article.id)
                             .filter_by(category_id=category, is_beginner=True))
    beginner_links = [{'name': bl[0], 'link': '/articles/' + bl[1]}
                      for bl in query_beginner.all()]

    # Vérifier que la catégorie existe
    if len(categories) == 1:
    # Renvoyer les informations ou une erreur
        category = categories[0]
        data = {
            "page_type": category.id,
            "name": category.name,
            "description": category.description,
            "beginner_links": beginner_links,
            "tags": [
              {
                "name": "1-balles",
                "description": "Blabla de description",
                "articles": [
                  {
                    "name": "Apprendre le 1 balles",
                    "description": "Longue description de comment faire",
                    "id": "apprendre-le-1-balles"
                  },
                  {
                    "name": "Apprendre le 2 balles",
                    "description": "Longue description de comment faire",
                    "id": "2-balles.html"
                  },
                ]
              }
            ]
          }
        return render_template('general-template.html', data=data, 
                               type_js='category')
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

        # Récupération des tags. Si le tag n'existe pas, on le créé
        tags = []
        tags_name = request.form['tags'].split(',')
        for tag_name in tags_name:
            query = session.query(Tag).filter_by(id=tag_name)
            current_tags = query.all()
            if len(current_tags) == 1:
                tags.append(current_tags[0])
            else:
                tags.append(Tag(name=tag_name, id=tag_name.lower()))

        is_beginner = (True if request.form['is_beginner'] == 'True'
                       else False)
        article = Article(
            name=request.form['name'], author=request.form['author'],
            content=request.form['content'], category_id=request.form['category'],
            creation_date=now, last_modification_date=now,
            description=request.form['description'], id=id_art, tags=tags,
            is_beginner=is_beginner)
        session.add(article)
        session.commit()
        return Response("Article enregistré")
