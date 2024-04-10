from flask_restful_swagger_3 import Schema


class ResponseBase(Schema):
    properties = {
        'status': {
            'type': 'boolean',
        },
        'message': {
            'type': 'string'
        },
    }
    required = ['status', 'message']


class ResponseBadRequest(Schema):
    properties = {
        **ResponseBase.properties,
        'errors': {
            'type': 'object',
        },
    }
    required = ['status', 'message']


class ParmsPagination(Schema):
    properties = {
        'limit': {
            'type': 'integer',
            'format': 'int64',
        },
        'page': {
            'type': 'integer',
            'format': 'int64',
        },
    }


params_pagination = [
    {
        'in': 'query',
        'name': 'pagination',
        'schema': ParmsPagination,
        'description': 'pagination data'
    }]


class PaginationResponse(Schema):
    properties = {
        'current_page': {
            'type': 'integer',
            'format': 'int64',
        },
        'total_pages': {
            'type': 'integer',
            'format': 'int64',
        },
        'total_items': {
            'type': 'integer',
            'format': 'int64',
        },
    }


