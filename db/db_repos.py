from sqlalchemy.exc import IntegrityError
import logging
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION, UNIQUE_VIOLATION

from db.db_models import UserDB, WalletDB
from exception import AlreadyExistsException
from schemas import User, Wallet
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: AsyncSession):
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
                f"Error while creating User. Details: {error.orig.args}"
            )
            await self._db_session.rollback()
            await self.__integrity_error_handler(error, user_data)

    @staticmethod
    async def __integrity_error_handler(
        e: IntegrityError, user: User
    ) -> None:
        if e.orig.sqlstate == UNIQUE_VIOLATION:
            if "telegram_id" in e.orig.args[0]:
                raise AlreadyExistsException(
                    f"Already exist this telegram id: {user.telegram_id}"
                )


class WalletRepository:
    def __init__(self, db_session: AsyncSession):
        self._db_session = db_session

    async def create_wallet_by_user_id(self, user_id: int) -> Wallet:
        wallet_db = WalletDB(user_id=user_id)
        self._db_session.add(wallet_db)

        try:
            await self._db_session.commit()
            await self._db_session.refresh(wallet_db)
            return Wallet.from_orm(wallet_db)
        except IntegrityError as error:
            logger.error(
                f"Error while creating Wallet. Details: {error.orig.args}"
            )
            await self._db_session.rollback()

    @staticmethod
    async def __integrity_error_handler(
        e: IntegrityError, user: User
    ) -> None:
        if e.orig.sqlstate == FOREIGN_KEY_VIOLATION:
            if "telegram_id" in e.orig.args[0]:
                raise AlreadyExistsException(
                    f"Already exist this telegram id: {user.telegram_id}"
                )
