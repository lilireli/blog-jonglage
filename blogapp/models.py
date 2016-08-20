# coding: utf-8

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Table

#Categories
CATEGORIES = ['acrobatie', 'balles', 'staff']

# Information de connexion
engine = create_engine('mysql://pierrick:@localhost/jonglage')
Session = sessionmaker(bind=engine)
Base = declarative_base()

article_to_tag = Table('article_to_tag', Base.metadata,
                       Column('article_id', String(50), ForeignKey('articles.id')),
                       Column('tag_name', String(50), ForeignKey('tags.name')))

class Category(Base):
    __tablename__ = 'categories'

    name = Column(String(30), primary_key=True)
    url = Column(String(50))
    articles = relationship("Article", back_populates="category")

    def __repr__(self):
        return "<Category(name='{name}'>".format(name=self.name)

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    author = Column(String(30))
    content = Column(String(10000))
    description = Column(String(500))
    creation_date = Column(Date)
    last_modification_date = Column(Date)
    category_name = Column(String(30), ForeignKey('categories.name'))

    category = relationship('Category', back_populates='articles')
    tags = relationship('Tag', secondary=article_to_tag,
                        back_populates="articles")

class Tag(Base):
    __tablename__ = 'tags'

    name = Column(String(50), primary_key=True)

    articles = relationship('Article', secondary=article_to_tag,
                            back_populates='tags')
    

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session()
    for category in CATEGORIES:
        ed_category = Category(name=category)
        session.add(ed_category)

    session.commit()
