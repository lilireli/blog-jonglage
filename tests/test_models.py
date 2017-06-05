# coding: utf-8

from io import BytesIO

from .conftest import headers_authorization
from blogapp.models import Category


def test_get_tags_and_beginner_links(client, test_db, truncate):
    # Creation of the category
    data_to_post_create = {'name': 'a test category',
                           'description': 'test category'}
    client.post('/categories/create', headers=headers_authorization,
                data=data_to_post_create)

    # Creation of the articles
    # Article beginner
    data_to_post = {"name": "article beginner",
                    "author": "a test author",
                    "content": (BytesIO(b'a test content'), 'test.txt'),
                    "category": "a-test-category",
                    "is_beginner": "True",
                    "tags": "tag1,tag3",
                    "description": "a test beginner description",
                    "difficulty": "5"}
    client.post('/articles/create', data=data_to_post,
                headers=headers_authorization)

    # Article no beginner
    data_to_post = {"name": "article no beginner",
                    "author": "a test author",
                    "content": (BytesIO(b'a test content'), 'test.txt'),
                    "category": "a-test-category",
                    "is_beginner": "False",
                    "tags": "tag1,tag2",
                    "description": "a test no beginner description",
                    "difficulty": "3"}
    client.post('/articles/create', data=data_to_post,
                headers=headers_authorization)

    # Tests
    categories = test_db.session.query(Category).all()
    assert len(categories) == 1
    category = categories[0]

    beginner_links, tags = category.get_tags_and_beginner_links()

    assert len(beginner_links) == 1
    beginner_link = beginner_links[0]
    assert beginner_link['name'] == 'article beginner'
    assert beginner_link['link'] == '/articles/article-beginner'

    assert len(tags) == 3
    for tag in tags:
        assert tag['description'] == ''
        articles = tag['articles']
        if tag['name'] == 'tag1':
            assert len(articles) == 2
            assert articles[0]['id'] == 'article-no-beginner'
            assert articles[1]['id'] == 'article-beginner'
        elif tag['name'] == 'tag2':
            assert len(articles) == 1
            assert articles[0]['id'] == 'article-no-beginner'
        elif tag['name'] == 'tag3':
            assert len(articles) == 1
            assert articles[0]['id'] == 'article-beginner'
