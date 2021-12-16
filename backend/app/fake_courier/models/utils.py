from typing import List, Tuple, Dict, Type
from sqlalchemy import desc, nullslast, nullsfirst, func, select
from sqlalchemy.orm import Query


async def paginate_query(
    db,
    query: Query,
    model: Type,
    fields_names_map: Dict,
    relationship_properties: List,
    limit: int = None,
    offset: int = None,
    order_by: str = None,
) -> Tuple[List, Dict]:
    is_desc = False
    count = (await db.execute(select(func.count(model.id)))).scalars().one()

    pagination = {
        "count": count,
        "limit": limit,
        "offset": offset,
        "orderBy": order_by,
    }

    if order_by:
        is_desc = order_by.startswith("-")
        if is_desc:
            order_by = order_by[1:]
        order_by = fields_names_map.get(order_by, order_by)

    if order_by and order_by in relationship_properties:
        # all relationships have to be sorted on python side, native order_by doesn't return Model
        # with 0 count relationship because of OUTER LEFT JOIN made by ORM within joinloaded method
        results = (await db.execute(query)).scalars().all()
        results = sorted(results, key=lambda instance: getattr(instance, order_by), reverse=is_desc)
        if limit:
            limit = limit + offset
            results = results[:limit]
        if offset:
            offset = int(offset)
            results = results[offset:]
    else:
        if order_by:
            if is_desc:
                column_property = getattr(model, order_by)
                column_property = desc(column_property)
                column_property = nullslast(column_property)
            else:
                column_property = getattr(model, order_by)
                column_property = nullsfirst(column_property)
            query = query.order_by(column_property)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        results = (await db.execute(query)).scalars().all()
    await db.commit()
    return results, pagination
