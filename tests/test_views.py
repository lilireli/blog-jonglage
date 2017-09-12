# coding: utf-8

from io import BytesIO
import json
from time import sleep

from .conftest import headers_authorization
from blogapp.models import Article, Category, Tag
from blogapp.views import (convert_to_bool, identifize, get_or_create_tag,
                           get_nb_pages, get_index_articles, get_categories)

# Utils


def test_get_nb_pages(client, test_db, truncate):

    # Test without articles
    assert get_nb_pages() == 1

    # Creation of the categories
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    data_to_post_create_journal = {'name': 'journal',
                                   'description': 'journal category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create_journal)

    # Creation of the articles
    for i in range(25):
        data_to_post = {"name": "article {}".format(i),
                        "author": "a test author",
                        "content": (BytesIO(b"a test content"), "test.txt"),
                        "category": "a-test-category",
                        "is_beginner": "True",
                        "tags": "tag1,tag2",
                        "description": "a test description",
                     "difficulty": "5"}
        client.post('/articles/create', data=data_to_post,
                    headers=headers_authorization)

    for i in range(25, 30):
        data_to_post = {"name": "article {}".format(i),
                        "author": "a test journal author",
                        "content": (BytesIO(b"a test journal content"),
                                    "test_journal.txt"),
                        "category": "journal",
                        "is_beginner": "True",
                        "tags": "tag1,tag2",
                        "description": "a test journal description",
                        "difficulty": "5"}
        client.post('/articles/create', data=data_to_post,
                    headers=headers_authorization)

    # Tests
    assert get_nb_pages() == 2
    assert get_nb_pages(True) == 1


def test_get_index_articles(client, test_db, truncate):

    # Test without articles
    articles_0 = get_index_articles(1)
    assert not articles_0

    # Creation of the categories
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    data_to_post_create_journal = {'name': 'journal',
                                   'description': 'journal category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create_journal)

    # Creation of the articles
    for i in range(25):
        data_to_post = {"name": "article {}".format(i),
                        "author": "a test author",
                        "content": (BytesIO(b"a test content"), "test.txt"),
                        "category": "a-test-category",
                        "is_beginner": "True",
                        "tags": "tag1,tag2",
                        "description": "a test description",
                        "difficulty": "5"}
        client.post('/articles/create', data=data_to_post,
                    headers=headers_authorization)

    for i in range(25, 30):
        data_to_post = {"name": "article {}".format(i),
                        "author": "a test journal author",
                        "content": (BytesIO(b"a test journal content"),
                                    "test_journal.txt"),
                        "category": "journal",
                        "is_beginner": "True",
                        "tags": "tag1,tag2",
                        "description": "a test journal description",
                        "difficulty": "5"}
        client.post('/articles/create', data=data_to_post,
                    headers=headers_authorization)

    # Tests
    articles_1 = get_index_articles(1)
    assert len(articles_1) == 20
    articles_2 = get_index_articles(2)
    assert len(articles_2) == 10
    articles_3 = get_index_articles(1, True)
    assert len(articles_3) == 5
    assert articles_3[0]["author"] == "a test journal author"


def test_convert_to_bool():
    assert convert_to_bool('True')
    assert convert_to_bool('true')
    assert not convert_to_bool('false')


def test_identifize():
    assert identifize('Test') == 'test'
    assert identifize('test 2') == 'test-2'
    assert identifize('éèêàâîù') == 'eeeaaiu'


def test_get_or_create_tag(client, test_db, truncate):

    # Creation of the tag
    data_to_post_create = {'name': 'a get or create tag',
                           'description': 'test tag'}
    client.post('/tags/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    tags = get_or_create_tag(['a-get-or-create-tag', 'another tag'])
    assert len(tags) == 2
    assert tags[0].id == 'a-get-or-create-tag'
    assert tags[0].name == 'a get or create tag'
    assert tags[0].description == 'test tag'
    assert tags[1].id == 'another-tag'
    assert tags[1].name == 'another tag'
    assert tags[1].description == ''

    query = test_db.session.query(Tag).filter_by(id='another-tag')
    assert len([tag for tag in query]) == 1


def test_get_categories(client, test_db, truncate):

    # Creation of the categories
    data_to_post_create = {'name': 'a category non empty',
                           'description': 'test category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    data_to_post_create = {'name': 'another category non empty',
                           'description': 'test category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    data_to_post_create = {'name': 'an empty category',
                           'description': 'test category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    data_to_post_create = {'name': 'journal',
                           'description': 'journal category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the articles
    data_to_post = {"name": "a test article",
                    "author": "a test author",
                    "content": (BytesIO(b"a test content"), "test.txt"),
                    "category": "a-category-non-empty",
                    "is_beginner": "True",
                    "tags": "tag1,tag2",
                    "description": "a test description",
                    "difficulty": "5"}
    client.post('/articles/create', data=data_to_post,
                headers=headers_authorization)

    data_to_post = {"name": "a second test article",
                    "author": "a test author",
                    "content": (BytesIO(b"a test content"), "test.txt"),
                    "category": "another-category-non-empty",
                    "is_beginner": "True",
                    "tags": "tag1,tag2",
                    "description": "a test description",
                    "difficulty": "5"}
    client.post('/articles/create', data=data_to_post,
                headers=headers_authorization)

    categories_non_empty = get_categories()
    assert categories_non_empty == [{'id': 'journal', 'name': 'Journal'},
                                    {'id': 'a-category-non-empty',
                                     'name': 'a category non empty'},
                                    {'id': 'another-category-non-empty',
                                     'name': 'another category non empty'}]

# General routes


def test_index(client, test_db):
    assert client.get('/').status_code == 200


def test_about(client):
    assert client.get('/about').status_code == 200


def test_initialize(client, test_db):
    test_db.drop_all()
    assert (client.get('/initialize', headers=headers_authorization)
            .status_code == 200)
    with open('blogapp/categories.json') as json_data:
        for category in json.load(json_data):
            query = test_db.session.query(Category).filter_by(id=category['id'])
            assert len([cat for cat in query]) == 1

# Swagger routes


def test_swagger(client):
    assert client.get('/swagger/index.html',
                      headers=headers_authorization).status_code == 200

# Category routes


def test_get_category(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a get category',
                           'description': 'test category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    assert client.get('/categories/a-get-category').status_code == 200


def test_get_journal(client, test_db, truncate):
    # Creation of the category
    data_to_post_create = {'name': 'journal',
                           'description': 'test journal category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)
    assert client.get('/categories/journal').status_code == 200


def test_get_json_category(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a category for test json',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    response = client.get('/categories/a-category-for-test-json/json',
                          headers=headers_authorization)
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == {
        'name': 'a category for test json',
        'id': 'a-category-for-test-json',
        'description': 'test category'}


def test_modify_category(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a modify category',
                           'description': 'test category'}
    client.post('/categories/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    data_to_post = {'name': 'another category'}
    assert (client.post('/categories/a-modify-category/modify',
                        headers=headers_authorization, data=data_to_post)
            .status_code == 200)

    query_category = test_db.session.query(Category)
    categories = [cat for cat in query_category]
    assert len(categories) == 1
    category = categories[0]
    assert category.name == 'another category'
    assert category.id == 'a-modify-category'
    assert category.description == 'test category'


def test_create_category(client, test_db, truncate):

    # Tests
    data_to_post = {'name': 'a test category',
                    'description': 'test category'}

    assert client.post('/categories/create',
                       headers=headers_authorization,
                       data=data_to_post).status_code == 200

    query_category = test_db.session.query(Category)
    categories = [cat for cat in query_category]
    assert len(categories) == 1
    category = categories[0]
    assert category.name == 'a test category'
    assert category.id == 'a-test-category'
    assert category.description == 'test category'


def test_delete_category(client, test_db):

    # Creation of the category
    data_to_post_create = {'name': 'a delete category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    assert client.delete('/categories/a-delete-category/delete',
                         headers=headers_authorization).status_code == 200

    query_category = test_db.session.query(Category)
    categories = [cat for cat in query_category]
    assert len(categories) == 0


# Article routes


def test_get_article(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the article
    data_to_post = {"name": "a test article",
                    "author": "a test author",
                    "content": (BytesIO(b"a test content"), "test.txt"),
                    "category": "a-test-category",
                    "is_beginner": "True",
                    "tags": "tag1,tag2",
                    "description": "a test description",
                    "difficulty": "5"}

    client.post('/articles/create', data=data_to_post,
                headers=headers_authorization)

    # Tests
    response = client.get('/articles/a-test-article')
    assert response.status_code == 200

    # Article that not exist
    assert client.get('/articles/no-article').status_code == 404


def test_create_article(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    data_to_post = {"name": "a test article",
                    "author": "a test author",
                    "content": (BytesIO(b"a test content"), "test.txt"),
                    "category": "a-test-category",
                    "is_beginner": "True",
                    "tags": "tag1,tag2",
                    "description": "a test description",
                    "difficulty": "5",
                    "image": "a test image"}
    assert client.post("/articles/create",
                       headers=headers_authorization,
                       data=data_to_post).status_code == 200

    query_article = test_db.session.query(Article)
    articles = [article for article in query_article]
    assert len(articles) == 1
    article = articles[0]
    assert article.name == 'a test article'
    assert article.id == 'a-test-article'
    assert article.author == 'a test author'
    assert article.content == 'a test content'
    assert article.category.id == 'a-test-category'
    assert article.is_beginner
    assert article.description == 'a test description'
    assert article.difficulty == 5
    assert article.image == 'a test image'
    assert len(article.tags) == 2
    assert article.tags[0].id == 'tag1'
    assert article.tags[1].id == 'tag2'
    assert article.creation_date == article.last_modification_date


def test_get_json_article(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the article
    data_to_post_create = {"name": "an article for test json",
                           "author": "a test author",
                           "content": (BytesIO(b"a test content"), "test.txt"),
                           "category": "a-test-category",
                           "is_beginner": "True",
                           "tags": "tag1,tag2",
                           "description": "a test description",
                           "difficulty": "5",
                           "image": "a test image"}
    client.post('/articles/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    response = client.get('/articles/an-article-for-test-json/json',
                          headers=headers_authorization)
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == {
        'name': 'an article for test json',
        'id': 'an-article-for-test-json',
        'author': 'a test author',
        'content': 'a test content',
        'category_id': 'a-test-category',
        'is_beginner': True,
        'tags': 'tag1,tag2',
        'description': 'a test description',
        'difficulty': '5',
        'image': 'a test image'}


def test_modify_article(client, test_db, truncate):

    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the article
    data_to_post_create = {"name": "a modify article",
                           "author": "a test author",
                           "content": (BytesIO(b"a test content"), "test.txt"),
                           "category": "a-test-category",
                           "is_beginner": "True",
                           "tags": "tag1,tag2",
                           "description": "a test description",
                           "difficulty": "5"}
    client.post('/articles/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    # We must do that for have a different last_modification_date
    sleep(2)

    data_to_post = {"name": "another article",
                    "tags": "tag1,tag3"}
    assert (client.post('/articles/a-modify-article/modify',
                        headers=headers_authorization, data=data_to_post)
            .status_code == 200)

    query_article = test_db.session.query(Article)
    articles = [article for article in query_article]
    assert len(articles) == 1
    article = articles[0]
    assert article.name == 'another article'
    assert article.id == 'a-modify-article'
    assert article.author == 'a test author'
    assert article.content == 'a test content'
    assert article.category.id == 'a-test-category'
    assert article.is_beginner
    assert article.description == 'a test description'
    assert article.difficulty == 5
    assert article.image == ''
    assert len(article.tags) == 2
    assert article.tags[0].id == 'tag1'
    assert article.tags[1].id == 'tag3'
    assert article.creation_date != article.last_modification_date


def test_delete_article(client, test_db):

    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the article
    data_to_post_create = {"name": "a delete article",
                           "author": "a test author",
                           "content": (BytesIO(b"a test content"), "test.txt"),
                           "category": "a-test-category",
                           "is_beginner": "True",
                           "tags": "tag1,tag2",
                           "description": "a test description",
                           "difficulty": "5"}
    client.post('/articles/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    assert client.delete('articles/a-delete-article/delete',
                         headers=headers_authorization).status_code == 200

    query_article = test_db.session.query(Article)
    articles = [article for article in query_article]
    assert len(articles) == 0

# Tag routes


def test_get_json_tag(client, test_db, truncate):

    # Creation of the tag
    data_to_post_create = {'name': 'a tag for test json',
                           'description': 'test tag'}
    client.post('/tags/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    response = client.get('/tags/a-tag-for-test-json/json',
                          headers=headers_authorization)
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == {
        'name': 'a tag for test json',
        'id': 'a-tag-for-test-json',
        'description': 'test tag'}


def test_modify_tag(client, test_db, truncate):

    # Creation of the tag
    data_to_post_create = {'name': 'a modify tag',
                           'description': 'test tag'}
    client.post('/tags/create',
                headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    data_to_post = {'name': 'another tag'}
    assert (client.post('/tags/a-modify-tag/modify',
                        headers=headers_authorization, data=data_to_post)
            .status_code == 200)

    query_tag = test_db.session.query(Tag)
    tags = [tag for tag in query_tag]
    assert len(tags) == 1
    tag = tags[0]
    assert tag.name == 'another tag'
    assert tag.id == 'a-modify-tag'
    assert tag.description == 'test tag'


def test_create_tag(client, test_db, truncate):

    # Test with description
    data_to_post = {"name": "a test tag",
                    "description": "a tag description"}
    assert client.post("tags/create",
                       headers=headers_authorization,
                       data=data_to_post).status_code == 200
    query_tag = test_db.session.query(Tag)
    tags = [tag for tag in query_tag]
    assert len(tags) == 1
    tag = tags[0]
    assert tag.name == 'a test tag'
    assert tag.id == 'a-test-tag'
    assert tag.description == 'a tag description'

    # Test without description
    data_to_post = {"name": "a test tag without description"}
    client.post("/tags/create",
                headers=headers_authorization,
                data=data_to_post)
    query_tag = (test_db.session.query(Tag)
                        .filter(Tag.id == "a-test-tag-without-description"))
    tags = [t for t in query_tag]
    assert len(tags) == 1
    tag = tags[0]
    assert tag.description is None


def test_delete_tag(client, test_db):

    # Creation of the tag
    data_to_post_create = {'name': 'a delete tag'}
    client.post('/tags/create', headers=headers_authorization,
                data=data_to_post_create)

    # Tests
    assert client.delete('/tags/a-delete-tag/delete',
                         headers=headers_authorization).status_code == 200

    query_tag = test_db.session.query(Tag)
    tags = [tag for tag in query_tag]
    assert len(tags) == 0
