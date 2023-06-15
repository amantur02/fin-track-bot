from sqlalchemy.orm import Session
from schemas import User, Wallet, SuccessResponse
from db.db_repos import UserRepository, WalletRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_wallet_services(
        user_data: User, db_session: AsyncSession
) -> SuccessResponse:
    user_repo = UserRepository(db_session)
    wallet_repo = WalletRepository(db_session)

    user = await user_repo.create_user(user_data)
    await wallet_repo.create_wallet_by_user_id(user.id)

    return SuccessResponse(message="Successfully create wallet")
