from sqlalchemy import Column, Integer, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from bot.db.base import Base


class PlayerScore(Base):
    __tablename__ = "playerscore"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    score = Column(Integer, default=0)


class Lang(Base):
    __tablename__ = 'lang'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    user = relationship("User", backref="lang")
    word = relationship("Word", backref="lang")


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    user = relationship("User", backref="role")
    name = Column(String)
    code = Column(String)


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    notification = Column(Integer, default=0)
    lang_id = Column(Integer, ForeignKey('lang.id'))
    role_id = Column(Integer, ForeignKey('role.id'))


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    word = relationship("Word", backref="tag")
    label = Column(String)


class Word(Base):
    __tablename__ = "word"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    translate_id = Column(Integer, ForeignKey('lang.id'))
    original = Column(String)
    transcription = Column(String)
    translate = Column(String)
    audio_id = Column(BigInteger, unique=True, autoincrement=False, nullable=True)
    image_id = Column(BigInteger, unique=True, autoincrement=False, nullable=True)
    tag_id = Column(Integer, ForeignKey('tag.id'))
    # * Английский вариант
    # * Транскрипция
    # * Русский
    # * Казахский
    # * Ид аудио в тг английский/русский/казахский
    # * Статус
    # * Рейтинг
    # * Тэги
    # * ? Картинка
