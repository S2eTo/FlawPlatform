from rest_framework.pagination import PageNumberPagination


class CommonPageNumberPagination(PageNumberPagination):

    def __init__(self, page_size=10, max_page_size=10, page_query_param='page'):
        self.page_size = page_size
        self.max_page_size = max_page_size
        self.page_query_param = page_query_param
