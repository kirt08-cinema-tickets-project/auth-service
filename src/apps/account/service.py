from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession 

from src.core.db.models import (
    PendingContactChangesRequest,
    PendingContactChangesResponse,
    PendingContactChangesORM,
)

from src.core.db.models.utils import Type

async def service_find_PendingChange(
    account_id : int,
    type : Type,
    session : AsyncSession,
) -> PendingContactChangesResponse:
    res = ( await session.execute(select(PendingContactChangesORM)
                                  .filter_by(account_id = account_id,
                                             type = type))).scalar_one()
    return PendingContactChangesResponse.model_validate(res)

async def service_upsert_PendingChange(
    account_id : int,
    data: PendingContactChangesRequest,
    session: AsyncSession,
) -> bool:
    query = insert(PendingContactChangesORM).values(
        account_id = account_id,
        type = data.type,
        value = data.value,
        codeHash = data.codeHash,
        expiresAt = data.expiresAt,
    )

    update_dict = {
        "value": query.excluded.value, 
        "codeHash": query.excluded.codeHash, 
        "expiresAt": query.excluded.expiresAt,
    }

    query = query.on_conflict_do_update(
        index_elements=["account_id", "type"],
        set_=update_dict,
    ).returning(PendingContactChangesORM)

    res = (await session.execute(query)).scalar_one()
    await session.commit()
    return True

async def service_delete_PendingChange(
    account_id : int,
    type : Type,
    session : AsyncSession,
): 
    result = await session.execute(
            delete(PendingContactChangesORM)
            .filter_by(
                account_id = account_id,
                type = type
            )
    )
    await session.commit()
    return result
    