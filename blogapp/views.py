# coding: utf-8

import json
import datetime
import unicodedata
import locale
from collections import defaultdict

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

locale.setlocale(locale.LC_TIME, "fr_FR.utf8")

NB_ARTICLES_BY_PAGE = 20
DATE_STRING_FORMAT = "%d %b %Y"

def tranform_article(article):
    tags = [{"name": tag.name} for tag in article.tags]
    article_dict = {"name": article.name,
                    "creation_date": article.creation_date.strftime(DATE_STRING_FORMAT),
                    "author": article.author,
                    "description": article.description,
                    "id": article.id,
                    "category": article.category_id,
                    "tags": tags}
    return article_dict


@app.route('/')
@app.route('/page/<int:page>')
def index(page=1):
    nb_page = ((session.query(Article).count() -1 )
               / NB_ARTICLES_BY_PAGE) + 1
    pages = [{"number": i, "link": "/page/" + str(i)}
             for i in range(1, nb_page + 1)]
    query_articles = (session.query(Article)
                             .order_by(Article.creation_date.desc()))
    articles = [tranform_article(art) for art
                in query_articles[(page - 1) * NB_ARTICLES_BY_PAGE:page * NB_ARTICLES_BY_PAGE]]
    data = {
        "page_type": "home",
        "pagination": {
          "current_page": page,
          "nb_page": nb_page,
          "pages": pages
        },
        "articles": articles
    }
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
        articles = category.articles
        articles_by_tags = defaultdict(list)
        for article in articles:
            for tag in article.tags:
                articles_by_tags[(tag.id, tag.name)].append(
                    {"name": article.name, "description": article.description,
                     "id": article.id})
        tags = [{"name": k[0], "description": k[1], "articles": v}
                for k, v in articles_by_tags.items()]
        data = {
            "page_type": category.id,
            "name": category.name,
            "description": category.description,
            "beginner_links": beginner_links,
            "tags": tags
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
            "last_modification_date": article.last_modification_date.strftime(
                DATE_STRING_FORMAT),
            "tags": tags,
        }
        return render_template('general-template.html', data=json.dumps(data),
                               type_js='article')
    else:
        return 'error'


@app.route('/articles/create', methods=["POST"])
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
            content=request.form['content'],
            category_id=request.form['category'], creation_date=now,
            last_modification_date=now, is_beginner=is_beginner,
            description=request.form['description'], id=id_art, tags=tags)
        session.add(article)
        session.commit()
        return Response("Article enregistré")


@app.route('/tags/<tag_id>/json')
def get_json_tag(tag_id):
    query = session.query(Tag).filter_by(id=tag_id)
    tags = query.all()
    if len(tags) == 1:
        tag = tags[0]
        tag_dict = {"name": tag.name, "id": tag.id,
                    "description": tag.description}
        return str(tag_dict)
    else:
        return 'error'


@app.route('/tags/<tag_id>/modify', methods=['POST'])
def modify_tag(tag_id):
    if request.method == 'POST':
        query = session.query(Tag).filter_by(id=tag_id)
        tags = query.all()
        if len(tags) == 1:
            tag = tags[0]
            tag.name = (request.form['name']
                        if 'name' in request.form else tag.name)
            tag.description = (request.form['description']
                               if 'description' in request.form
                               else tag.description)
            session.commit()
            return 'Tag modifié'
        else:
            return 'error'

@app.route('/tags/create', methods=['POST'])
def create_tag():
    if request.method == 'POST':
        tag = Tag(name=request.form['name'],
                  description=request.form['description'],
                  id=request.form['name'].lower())
        session.add(tag)
        session.commit()
        return Response("Tag enregistré")


@app.route('/tags/<tag_id>/delete', methods=['DELETE'])
def delete_tag(tag_id):
    if request.method == 'DELETE':
        query = session.query(Tag).filter_by(id=tag_id)
        tags = query.all()
        if len(tags) == 1:
            tag = tags[0]
            session.delete(tag)
            session.commit()
            return Response("Tag supprimé")
        else:
            return 'error'
