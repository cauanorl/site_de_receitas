import math


def make_pagination_range(page_range, number_of_pages, current_page):
    total_pages = len(page_range)
    middle_range = math.ceil(number_of_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    if start_range < 0:
        start_range = 0
        stop_range = number_of_pages

    if (current_page + middle_range) > total_pages:
        sub_for_new_start_range = total_pages - stop_range
        start_range += sub_for_new_start_range

    pagination = page_range[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'number_of_pages': number_of_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
