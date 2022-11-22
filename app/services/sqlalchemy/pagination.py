def pagination_info(pagination_result):
    """Return pagination info"""

    try:
        info = {
            "has_next": pagination_result.has_next,
            "has_prev": pagination_result.has_prev,
            "next_num": pagination_result.next_num,
            "prev_num": pagination_result.prev_num,
            "current_page": pagination_result.page,
            "total_pages": pagination_result.pages,
            "per_page": pagination_result.per_page,
            "total_items": pagination_result.total
        }
    except:
        info = {}

    return info
