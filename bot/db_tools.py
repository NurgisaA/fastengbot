from sqlalchemy import select


async def get_or_create(session, model, **kwargs):
    async with session() as s:
        request = await s.execute(select(model).filter_by(**kwargs))
        a1 = request.scalars().first()
        if a1:
            return a1
        else:
            instance = model(**kwargs)
            await s.merge(instance)
            await s.commit()
            return instance
