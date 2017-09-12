# coding: utf-8

import json
import datetime
import unicodedata
import locale
import os
import shutil
import zipfile

from flask import (Flask, Response, render_template, request,
                   send_from_directory, Blueprint, current_app, abort)
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import markdown
import wget

from .models import Category, Article, Tag
from .database import db

tags_blueprint = Blueprint('tags', __name__)
articles_blueprint = Blueprint('articles', __name__)
categories_blueprint = Blueprint('categories', __name__)
general_blueprint = Blueprint('general', __name__)

# Use $abc$ for templates instead of {{abc}} because of conflict with vue.js
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='$$',
        block_end_string='$$',
        variable_start_string='$',
        variable_end_string='$',
        comment_start_string='$#',
        comment_end_string='#$',
    ))

def create_app(test=False):
    app = CustomFlask('__app__', template_folder='blogapp/templates',
                static_folder='blogapp/static', instance_relative_config=True)

    # Load the default configuration
    app.config.from_pyfile('../config/default.py')

    if not test:
        # Load the configuration from the instance folder (not versioned)
        app.config.from_pyfile('config.py')

        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default
        # configuration
        app.config.from_envvar('APP_CONFIG_FILE')

    else:
        app.config.from_pyfile('../config/test.py')

    # Set the locale to send datetime with locale format
    locale.setlocale(locale.LC_TIME, app.config['LOCALE'])

    app.register_blueprint(tags_blueprint, url_prefix='/tags')
    app.register_blueprint(articles_blueprint, url_prefix='/articles')
    app.register_blueprint(categories_blueprint, url_prefix='/categories')
    app.register_blueprint(general_blueprint)

    # Connexion information
    if 'DB_PASSWORD' in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            app.config['SQLALCHEMY_DATABASE_URI']
            .replace(':@', ':' + app.config['DB_PASSWORD'] + '@'))
    db.init_app(app)
    return app

# Authentication
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """ Verify that the username given is good. We use here a token, so the
     password is useless"""
    if not username or username != current_app.config['TOKEN']:
        return False
    return True

# Utils


def get_index_articles(page, journal=False):
    """Retrieving and formatting of the articles
    """
    if not journal:
        query_articles = (db.session.query(Article)
                          .order_by(Article.creation_date.desc()))
    else:
        query_articles = (db.session.query(Article)
                          .filter_by(category_id='journal')
                          .order_by(Article.creation_date.desc()))
    articles = [art.to_data(current_app.config['DATE_STRING_FORMAT']) for art
                in query_articles[
                    (page - 1) * current_app.config['NB_ARTICLES_BY_PAGE']:
                    page * current_app.config['NB_ARTICLES_BY_PAGE']]]
    return articles


def get_nb_pages(journal=False):
    # The total number of pages
    if not journal:
        nb_pages = ((db.session.query(Article).count() - 1)
                    // current_app.config['NB_ARTICLES_BY_PAGE']) + 1
    else:
        nb_pages = ((db.session.query(Article).filter_by(category_id='journal')
                     .count() - 1)
                    // current_app.config['NB_ARTICLES_BY_PAGE']) + 1
    # Even if there is no articles, we must have one page
    nb_pages = 1 if nb_pages == 0 else nb_pages
    return nb_pages


def convert_to_bool(bool):
    """ Convert a string into boolean
    """
    return True if (bool == 'True' or bool == 'true') else False


def identifize(name):
    """ Transform a name into id (lower and replace spaces into dashes)
    """
    # The id is the name lowered and without accent
    id_art = name.lower()
    id_art = id_art.replace(' ', '-')

    # allows to remove accents
    nfkd_form = unicodedata.normalize('NFKD', id_art)
    id_art = nfkd_form.encode('ASCII', 'ignore')
    return str(id_art, 'utf-8')


def get_or_create_tag(tags_name):
    """Retrieve of the tags. If it doesn't exist, it is created
    """
    tags = []
    for tag_name in tags_name:
        query = db.session.query(Tag).filter_by(id=tag_name)
        current_tags = query.all()
        # We retrieve the tag if it exists
        if len(current_tags) == 1:
            tags.append(current_tags[0])
        # Else we create it
        else:
            tag = Tag(name=tag_name,
                      id=identifize(tag_name),
                      description='')
            db.session.add(tag)
            db.session.commit()
            tags.append(tag)
    return tags


def get_categories():
    """ Retrieve all categories which have existing articles. We put journal
    first, and then sort the other by alhabetical order
    """
    query_cat = db.session.query(Category)
    categories = query_cat.all()

    # If the query send anything, we have a non-empty list, which is True
    categories_filtered = [
        {'id': cat.id, 'name': cat.name} for cat in categories
        if db.session.query(Article).filter_by(category_id=cat.id).all()
        if cat.id != 'journal']

    # We want the journal to be first, the other categories to be in
    # alphabetical order
    journal_category = [{'id': 'journal', 'name': 'Journal'}]
    categories_all = journal_category + sorted(journal_category,
                                               key=lambda cat: cat['name'])
    return categories_all

# Index route


@general_blueprint.route('/')
@general_blueprint.route('/page/<int:page>')
def index(page=1):
    """ Return the last articles for the selectionned page
    """

    # Get the total number of pages
    nb_pages = get_nb_pages()

    articles = get_index_articles(nb_pages)

    # The data with wich fill in the page
    data = {
        "page_type": "home",
        "page_category": "home",
        "nav_categories": get_categories(),
        "pagination": {
          "current_page": page,
          "nb_page": nb_pages
        },
        "articles": articles
    }
    return render_template('general-template.html', data=json.dumps(data))


@general_blueprint.route('/about')
def about():
    # The data with wich fill in the page
    data = {
        "page_type": "about",
        "nav_categories": get_categories()
    }

    return render_template('general-template.html', data=json.dumps(data))


@general_blueprint.route('/initialize')
@auth.login_required
def initialize():
    """ Initialize the database (creation of table, fill in with categories...)
    """
    # Creation of the database
    db.create_all()
    with open('blogapp/categories.json') as json_data:
        for category in json.load(json_data):
            query = db.session.query(Category).filter_by(id=category['id'])
            if not query.all():
                ed_category = Category(id=category['id'], name=category['name'],
                                       description=category['description'])
                db.session.add(ed_category)

    db.session.commit()

    # Copy of the useful static file for application
    if current_app.config['STATIC_FOLDER'] != 'blogapp/static':
        # We delete qll if it qlreqdy exists
        if os.path.exists(current_app.config['STATIC_FOLDER']):
            shutil.rmtree(current_app.config['STATIC_FOLDER'])
        shutil.copytree('blogapp/static', current_app.config['STATIC_FOLDER'])

    # Download of the external static file
    with open('config/to_download.json') as json_download:
        for folder, files in json.load(json_download).items():
            download_folder = os.path.join(current_app.config['STATIC_FOLDER'],
                                           folder)
            # Allow to includ the lib floder, which doesn't exists
            if not os.path.exists(download_folder):
                os.mkdir(download_folder)
            for file, url in files.items():
                if not os.path.isfile(os.path.join(
                    current_app.config['STATIC_FOLDER'], folder, file)):
                    wget.download(url, os.path.join(download_folder, file))
                    if file.endswith('zip'):
                        with zipfile.ZipFile(os.path.join(download_folder, file),
                                             'r') as zip_ref:
                            zip_ref.extractall(download_folder)
    return Response('Database and static folder initialized')


@general_blueprint.route('/upload/<path:type>', methods=['POST'])
@auth.login_required
def upload_file(type):
    """ Upload a static file. The location is took from the configuration.
    If we are in dev, this is the default static folder. Else, this will be
    a folder served by another sever (nginx for example)
    """
    if request.method == 'POST':
        upload_folder = os.path.join(os.getcwd(),
                                     current_app.config['STATIC_FOLDER'])
        if not os.path.exists(os.path.join(upload_folder, type)):
            os.mkdir(os.path.join(upload_folder, type))
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(upload_folder, type, filename))
    return Response('File uploaded')

# Swagger


@general_blueprint.route('/swagger/<path:filename>')
@auth.login_required
def swagger(filename):
    return send_from_directory(
        'blogapp/swagger', filename)

# Routes for categories (retrieve in JSON and HTML, modify, delete, create)


@categories_blueprint.route('/<category>')
def get_category(category):
    """ Send the HTML page for a category with all its articles
    """
    # Retrieving the information about the categories
    query_cat = db.session.query(Category).filter_by(id=category)
    categories = query_cat.all()

    # Verification that the category exists
    if len(categories) == 1:
        category = categories[0]
        beginner_links, tags = category.get_tags_and_beginner_links()

        # The data with wich fill in the page
        data = {
            "page_type": "category",
            "page_category": category.id,
            "nav_categories": get_categories(),
            "name": category.name,
            "description": category.description,
            "beginner_links": beginner_links,
            "tags": tags
          }
        return render_template('general-template.html', data=json.dumps(data))
    # If there is no categories, send an error
    else:
        abort(404)


@categories_blueprint.route('/journal')
@categories_blueprint.route('/journal/<int:page>')
def get_journal(page=1):
    """ Return the last articles for the selectionned page in journal category
    """
    # Retrieving the information about the journal category
    query_cat = db.session.query(Category).filter_by(id='journal')
    categories = query_cat.all()
    category = categories[0]

    # Get the total number of pages
    nb_pages = get_nb_pages(journal=True)

    articles = get_index_articles(nb_pages, journal=True)

    # The data with wich fill in the page
    data = {
        "name": category.name,
        "description": category.description,
        "page_type": "category",
        "page_category": "journal",
        "nav_categories": get_categories(),
        "pagination": {
          "current_page": page,
          "nb_page": nb_pages
        },
        "articles": articles
    }
    return render_template('general-template.html', data=json.dumps(data))


@categories_blueprint.route('/<category_id>/json')
@auth.login_required
def get_json_category(category_id):
    """ Retrieve a category on JSON. Useful to modify it after
    """
    query = db.session.query(Category).filter_by(id=category_id)
    categories = query.all()
    if len(categories) == 1:
        return categories[0].to_json()
    else:
        abort(404)


@categories_blueprint.route('/<category_id>/modify', methods=['POST'])
@auth.login_required
def modify_category(category_id):
    """ Modify a category. All the fields are optionnal
    """
    if request.method == 'POST':
        query = db.session.query(Category).filter_by(id=category_id)
        categories = query.all()
        if len(categories) == 1:
            category = categories[0]
            category.name = (request.form['name']
                             if 'name' in request.form else category.name)
            category.description = (request.form['description']
                                    if 'description' in request.form
                                    else category.description)
            db.session.commit()
            return Response('Category modified')
        else:
            abort(404)


@categories_blueprint.route('/create', methods=['POST'])
@auth.login_required
def create_category():
    """ Creation of a category
    """
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            description=request.form['description'],
                            id=identifize(request.form['name']))
        db.session.add(category)
        db.session.commit()
        return Response('Category saved')


@categories_blueprint.route('/<category_id>/delete', methods=['DELETE'])
@auth.login_required
def delete_category(category_id):
    """ Deletion of a category
    """
    if request.method == 'DELETE':
        query = db.session.query(Category).filter_by(id=category_id)
        categories = query.all()

        # Verification that the category exists
        if len(categories) == 1:
            category = categories[0]
            db.session.delete(category)
            db.session.commit()
            return Response('Category deleted')

        # If there is no categories, or more than one return an error
        else:
            abort(404)

# Routes for articles (retrieve in HTML and JSON, modify, delete, create)


@articles_blueprint.route('/<article>')
def get_article(article):
    # Retrieve the informations on the article
    query = db.session.query(Article).filter_by(id=article)
    articles = query.all()

    # Verify the number of articles
    if len(articles) == 1:
        article = articles[0]
        tags = [{"name": t.name} for t in article.tags]

        # Use parser to transform markdown into HTML
        content_html = markdown.markdown(article.content)

        # The data with wich fill in the page
        data = {
            "name": article.name,
            "author": article.author,
            "description": article.description,
            "url": article.id,
            "category": article.category.name,
            "page_type": "article",
            "page_category": article.category.id,
            "nav_categories": get_categories(),
            "content": content_html,
            "difficulty": article.difficulty,
            "image": article.image,
            "creation_date": article.creation_date.strftime(
                current_app.config['DATE_STRING_FORMAT']),
            "last_modification_date": (article.last_modification_date
                                       .strftime(
                                            current_app.config['DATE_STRING_FORMAT'])),
            "tags": tags,
        }
        return render_template('general-template.html', data=json.dumps(data))

    # If there is no articles, return an error
    else:
        abort(404)


@articles_blueprint.route('/create', methods=["POST"])
@auth.login_required
def create_article():
    """ Create an article. The creation_date and the last_modification_date
    are filled with the moment at which the request is received
    """
    if request.method == "POST":
        now = datetime.datetime.now()

        id_art = identifize(request.form['name'])

        # Retrieve of the tags. If it doesn't exist, it is created
        tags = get_or_create_tag(request.form['tags'].split(','))

        is_beginner = convert_to_bool(request.form['is_beginner'])

        article = Article(
            name=request.form['name'], author=request.form['author'],
            content=request.files['content'].read(),
            category_id=request.form['category'], creation_date=now,
            last_modification_date=now, is_beginner=is_beginner,
            description=request.form['description'], id=id_art, tags=tags,
            difficulty=request.form['difficulty'],
            image=request.form['image'] if 'image' in request.form else '')
        db.session.add(article)
        db.session.commit()
        return Response('Article saved')


@articles_blueprint.route('/<article_id>/json')
@auth.login_required
def get_json_article(article_id):
    """ Retrieve an article on JSON. Useful to modify it after
    """
    query = db.session.query(Article).filter_by(id=article_id)
    articles = query.all()
    if len(articles) == 1:
        return articles[0].to_json()
    else:
        abort(404)


@articles_blueprint.route('/<article_id>/modify', methods=['POST'])
@auth.login_required
def modify_article(article_id):
    """ Modification of an article. The last_modification_date is also updated
    """
    if request.method == 'POST':
        # Useful for the last_modification_date
        now = datetime.datetime.now()

        # Retrieve the article
        query = db.session.query(Article).filter_by(id=article_id)
        articles = query.all()

        # Verify the number of articles
        if len(articles) == 1:
            article = articles[0]
            article.name = (request.form['name']
                            if 'name' in request.form else article.name)
            article.description = (request.form['description']
                                   if 'description' in request.form
                                   else article.description)
            article.author = (request.form['author']
                              if 'author' in request.form
                              else article.author)
            article.content = (request.files['content'].read()
                               if 'content' in request.files
                               else article.content)
            article.is_beginner = (convert_to_bool(
                                       request.form['is_beginner'])
                                   if 'is_beginner' in request.form
                                   else article.is_beginner)
            article.category_id = (request.form['category_id']
                                   if 'category_id' in request.form
                                   else article.category_id)
            article.difficulty = (int(request.form['difficulty'])
                                  if 'difficulty' in request.form
                                  else article.difficulty)
            article.image = (request.form['image']
                             if 'image' in request.form
                             else article.image)

            # We have also to create the tags if they don't exist
            if 'tags' in request.form:
                tags = get_or_create_tag(request.form['tags'].split(','))
                article.tags = tags

            article.last_modification_date = now
            db.session.commit()
            return Response('Article modified')

        # If there is no articles, return an error
        else:
            abort(404)


@articles_blueprint.route('/<article_id>/delete', methods=['DELETE'])
@auth.login_required
def delete_article(article_id):
    """ Delete an article
    """
    if request.method == 'DELETE':
        query = db.session.query(Article).filter_by(id=article_id)
        articles = query.all()

        # Verify the number of articles
        if len(articles) == 1:
            article = articles[0]
            db.session.delete(article)
            db.session.commit()
            return Response("Article deleted")

        # If there is no articles, return an error
        else:
            abort(404)

# Routes for tags (retrieve in JSON and HTML, modify, delete, create)


@tags_blueprint.route('/<tag_id>/json')
@auth.login_required
def get_json_tag(tag_id):
    """ Retrieve a tag on JSON. Useful to modify it after
    """
    query = db.session.query(Tag).filter_by(id=tag_id)
    tags = query.all()
    if len(tags) == 1:
        return tags[0].to_json()
    else:
        abort(404)


@tags_blueprint.route('/<tag_id>/modify', methods=['POST'])
@auth.login_required
def modify_tag(tag_id):
    """ Modify a tag. All the fields are optionnal
    """
    if request.method == 'POST':
        query = db.session.query(Tag).filter_by(id=tag_id)
        tags = query.all()

        # Verify that the tag exist
        if len(tags) == 1:
            tag = tags[0]
            tag.name = (request.form['name']
                        if 'name' in request.form else tag.name)
            tag.description = (request.form['description']
                               if 'description' in request.form
                               else tag.description)
            db.session.commit()
            return 'Tag modified'

        # If there is no tags, return an error
        else:
            abort(404)


@tags_blueprint.route('/create', methods=['POST'])
@auth.login_required
def create_tag():
    """ Create a tag
    """
    if request.method == 'POST':
        description = (request.form['description']
                       if 'description' in request.form else None)

        tag = Tag(name=request.form['name'],
                  description=description,
                  id=identifize(request.form['name']))
        db.session.add(tag)
        db.session.commit()
        return Response('Tag saved')


@tags_blueprint.route('/<tag_id>/delete', methods=['DELETE'])
@auth.login_required
def delete_tag(tag_id):
    """ Delete a tag
    """
    if request.method == 'DELETE':
        query = db.session.query(Tag).filter_by(id=tag_id)
        tags = query.all()

        # Verify tag the tag exist
        if len(tags) == 1:
            tag = tags[0]
            db.session.delete(tag)
            db.session.commit()
            return Response('Tag deleted')

        # If there is no tags, return an error
        else:
            abort(404)
