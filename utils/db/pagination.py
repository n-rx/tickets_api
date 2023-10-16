"""
The sql_paginated function performs paginated SQL queries and returns the results as a dictionary.

This function takes an SQL query, page number, and the number of items per page as input.
It executes the query with pagination parameters and calculates the total number of pages
based on the total items. The result is returned as a dictionary containing the paginated items,
current page, items per page, and total pages.

Parameters:
    - query (str): The SQL query to be executed with pagination.
    - page (int): The current page number.
    - items_per_page (int): The number of items to be displayed per page.

Returns:
    dict: A dictionary containing the paginated items, page information, and total pages.
"""

from sqlalchemy import text
from API import db


def sql_paginated(query, page, items_per_page):
    """
    Executes a paginated SQL query and returns the results.

    Args:
        query (str): The SQL query to be executed with pagination.
        page (int): The current page number.
        items_per_page (int): The number of items to be displayed per page.

    Returns:
        dict: A dictionary containing paginated items, page, items per page, and total pages.
    """
    offset = (page - 1) * items_per_page

    sql = text(f"{query} LIMIT :items_per_page OFFSET :offset")
    result = db.engine.execute(sql, items_per_page=items_per_page, offset=offset)
    items = [dict(zip(tuple(result.keys()), i)) for i in result.cursor]

    total_items = db.session.execute(
        text(f"SELECT COUNT(*) FROM ({query}) as subquery")
    ).scalar()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    response = {
        "items": items,
        "page": page,
        "items_per_page": items_per_page,
        "total_pages": total_pages,
    }

    return response
