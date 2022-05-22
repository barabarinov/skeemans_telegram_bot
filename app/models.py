from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User():
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    statistics = relationship(
        'Statistic', back_populates='user',
        cascade='all, delete',
        lazy='dynemic',
        passive_deletes=True,
    )

    def __repr__(self):
        return f'User {self.first_name} {self.last_name} with username {self.username}'


class Statistic(Base):
    __table__ = 'statistics'

    user_id = Column(Integer, ForeignKey('users.telegram_id', ondelete='CASCADE'))
    button = Column(String(64), nullable=True)
    pressing_time = Column(DateTime, nullable=False, default=datetime.now())

    user = relationship(
        'User', back_pupulates='statistics',
        cascade='all, delete',
        lazy='dynemic',
        passive_deletes=True,
    )

    def __repr__(self):
        return f'Button name is {self.button}'
