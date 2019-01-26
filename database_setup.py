from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Subject(Base):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Course(Base):
    __tablename__ = 'course'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    summary = Column(String(250))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    subject = relationship(Subject)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'summary': self.summary,
        }


engine = create_engine('sqlite:///categories.db')

Base.metadata.create_all(engine)
