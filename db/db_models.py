from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql import expression

from db.db_base_class import Base


class UserDB(Base):
    __tablename__ = 'users'

    username = Column(String)
    telegram_id = Column(Integer, nullable=False, unique=True)


class WalletDB(Base):
    __tablename__ = 'wallets'

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    balance = Column(Integer, default=0, server_default='0')


class CategoryDB(Base):
    __tablename__ = 'categories'

    title = Column(String)


class WalletHistoryDB(Base):
    __tablename__ = 'wallet_histories'

    wallet_id = Column(
        Integer,
        ForeignKey("wallets.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    transaction = Column(Integer)
    is_deposit = Column(
        Boolean, default=True, server_default=expression.true()
    )
    comment = Column(String, nullable=True)

