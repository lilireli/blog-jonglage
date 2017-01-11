# coding: utf-8

import json
from collections import defaultdict

from database import db

# Table to link articles and tags
article_to_tag = db.Table('article_to_tag',
                          db.Column('article_id', db.String(50),
                                    db.ForeignKey('articles.id',
                                                  ondelete="CASCADE")),
                          db.Column('tag_id', db.String(50),
                                    db.ForeignKey('tags.id',
                                                  ondelete="CASCADE")))


class Category(db.Model):
    """ Categories of juggling (balles, staff...)
    """
    __tablename__ = 'categories'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(2000))

    articles = db.relationship("Article", back_populates="category")

    def to_json(self):
        """ Return a json of the class
        """
        category_json = {"name": self.name, "id": self.id,
                         "description": self.description}
        return json.dumps(category_json)

    def get_tags_and_beginner_links(self):
        # Retrieving the beginners links (articles which are
        # for beginners)
        query_beginner = (db.session.query(Article.name, Article.id)
                            .filter_by(category_id=self.id,
                                       is_beginner=True))
        beginner_links = [{'name': bl[0], 'link': '/articles/' + bl[1]}
                          for bl in query_beginner.all()]

        articles = self.articles
        articles_by_tags = defaultdict(list)

        # Formatting of articles and tags
        for article in articles:
            for tag in article.tags:
                articles_by_tags[(tag.name, tag.description)].append(
                    {"name": article.name, "description": article.description,
                     "id": article.id, "difficulty": int(article.difficulty)})
        tags = [{"name": k[0], "description": k[1],
                 "articles": sorted(v, key=lambda art: art['difficulty'])}
                for k, v in articles_by_tags.items()]
        return beginner_links, tags


class Article(db.Model):
    """ Contains the informations about an article
    """
    __tablename__ = 'articles'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(30))
    content = db.Column(db.String(10000))
    description = db.Column(db.String(500))
    creation_date = db.Column(db.DateTime)
    last_modification_date = db.Column(db.DateTime)
    is_beginner = db.Column(db.Boolean)
    difficulty = db.Column(db.Integer)
    category_id = db.Column(db.String(50), db.ForeignKey('categories.id',
                                                         ondelete="CASCADE"))

    category = db.relationship('Category', back_populates='articles')
    tags = db.relationship('Tag', secondary=article_to_tag,
                           back_populates="articles")

    def to_json(self):
        """ Return a json of the class
        """
        tags = ','.join([t.name for t in self.tags])
        article_json = {"id": self.id, "name": self.name,
                        "author": self.author, "content": self.content,
                        "is_beginner": self.is_beginner,
                        "description": self.description,
                        "category_id": self.category_id, "tags": tags,
                        "difficulty": str(self.difficulty)}
        return json.dumps(article_json)

    def to_data(self, date_format):
        """ Return a dict which will be used to fill in html page
        """
        tags = [{"name": tag.name} for tag in self.tags]
        article_dict = {"name": self.name,
                        "creation_date": self.creation_date.strftime(
                            date_format),
                        "author": self.author,
                        "description": self.description,
                        "id": self.id,
                        "category": self.category_id,
                        "tags": tags,
                        "difficulty": str(self.difficulty)}
        return article_dict


class Tag(db.Model):
    """ Contains the information on a tag
    """
    __tablename__ = 'tags'

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))

    articles = db.relationship('Article', secondary=article_to_tag,
                               back_populates='tags')

    def to_json(self):
        """ Return a json of the class
        """
        tag_json = {"name": self.name, "id": self.id,
                    "description": self.description}
        return json.dumps(tag_json)
