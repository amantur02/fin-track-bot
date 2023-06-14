from sqlalchemy.exc import IntegrityError
import logging
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from db_models import UserDB, WalletDB
from exception import NotFoundException, AlreadyExistsException
from schemas import User, Wallet
from sqlalchemy import select
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create_user(self, user_data: User) -> User:
        user_db = UserDB(
            **user_data.dict(exclude={'id'})
        )
        self._db_session.add(user_db)

        try:
            await self._db_session.commit()
            await self._db_session.refresh(user_db)
            return User.from_orm(user_db)
        except IntegrityError as error:
            logger.error(
                f"Error while creating Organization. Details: {error.orig.args}"
            )
            await self._db_session.rollback()
            await self.__integrity_error_handler(error, user_data)

    @staticmethod
    async def __integrity_error_handler(
        e: IntegrityError, user: User
    ) -> None:
        if e.orig.args == FOREIGN_KEY_VIOLATION:
            if "telegram_id" in e.orig.args[0]:
                raise AlreadyExistsException(
                    f"Already exist this telegram id: {user.telegram_id}"
                )
