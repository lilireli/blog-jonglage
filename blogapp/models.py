# coding: utf-8

import json

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Table, Boolean

# Connexion informations
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Table to link articles and tags
article_to_tag = Table('article_to_tag', Base.metadata,
                       Column('article_id', String(50),
                              ForeignKey('articles.id')),
                       Column('tag_id', String(50), ForeignKey('tags.id')))


class Category(Base):
    """ Categories of juggling (balles, staff...)
    """
    __tablename__ = 'categories'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(2000))

    articles = relationship("Article", back_populates="category")

    def to_json(self):
        """ Return a json of the class
        """
        category_json = {"name": self.name, "id": self.id,
                         "description": self.description}
        return str(category_json)


class Article(Base):
    """ Contains the informations about an article
    """
    __tablename__ = 'articles'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    author = Column(String(30))
    content = Column(String(10000))
    description = Column(String(500))
    creation_date = Column(DateTime)
    last_modification_date = Column(DateTime)
    is_beginner = Column(Boolean)
    difficulty = Column(Integer)
    category_id = Column(String(50), ForeignKey('categories.id'))

    category = relationship('Category', back_populates='articles')
    tags = relationship('Tag', secondary=article_to_tag,
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
        return str(article_json)

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


class Tag(Base):
    """ Contains the information on a tag
    """
    __tablename__ = 'tags'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(200))

    articles = relationship('Article', secondary=article_to_tag,
                            back_populates='tags')

    def to_json(self):
        """ Return a json of the class
        """
        tag_json = {"name": self.name, "id": self.id,
                    "description": self.description}
        return str(tag_json)
