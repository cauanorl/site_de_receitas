from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            number_of_pages=4,
            current_page=1
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        for page_number in range(1, 3):
            pagination = make_pagination_range(
                page_range=list(range(1, 21)),
                number_of_pages=4,
                current_page=page_number
            )['pagination']
            self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_sure_middle_ranges_are_correct(self):
        pages_and_required_range = [
            [10, [9, 10, 11, 12]],
            [16, [15, 16, 17, 18]]
        ]

        for page_number, range_required in pages_and_required_range:
            pagination = make_pagination_range(
                page_range=list(range(1, 21)),
                number_of_pages=4,
                current_page=page_number
            )['pagination']
            self.assertEqual(range_required, pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        for page_number in range(18, 22):
            pagination = make_pagination_range(
                page_range=list(range(1, 21)),
                number_of_pages=4,
                current_page=page_number
            )['pagination']
            self.assertEqual([17, 18, 19, 20], pagination)
