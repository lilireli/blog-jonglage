# coding: utf-8

import json

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Table, Boolean

# Information de connexion
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
Base = declarative_base()

article_to_tag = Table('article_to_tag', Base.metadata,
                       Column('article_id', String(50), ForeignKey('articles.id')),
                       Column('tag_id', String(50), ForeignKey('tags.id')))

class Category(Base):
    __tablename__ = 'categories'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(2000))

    articles = relationship("Article", back_populates="category")

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    author = Column(String(30))
    content = Column(String(10000))
    description = Column(String(500))
    creation_date = Column(Date)
    last_modification_date = Column(Date)
    is_beginner = Column(Boolean)
    category_id = Column(String(50), ForeignKey('categories.id'))

    category = relationship('Category', back_populates='articles')
    tags = relationship('Tag', secondary=article_to_tag,
                        back_populates="articles")

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    description = Column(String(200))

    articles = relationship('Article', secondary=article_to_tag,
                            back_populates='tags')
    

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    with open('blogapp/categories.json') as json_data:
        for category in json.load(json_data):
            ed_category = Category(id=category['name'], name=category['id'],
                                   description=category['description'])
            session.add(ed_category)

    session.commit()
