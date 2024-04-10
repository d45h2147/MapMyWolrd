from mapmyworld.docs.schemas import Schema, ResponseBase, PaginationResponse


class Category(Schema):
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'name': {
            'type': 'string'
        },
    }
    required = ['name']


class ResponseNewCategory(Schema):
    properties = {
        **ResponseBase.properties,
        'category': Category,
    }


class ResponseCategories(Schema):
    properties = {
        **ResponseBase.properties,
        'pagination': PaginationResponse,
        'data': Category.array(),
        'total': {
            'type': 'int'
        },
    }
