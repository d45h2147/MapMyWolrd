from mapmyworld.docs.schemas import Schema, ResponseBase, PaginationResponse, ParmsPagination
from mapmyworld.docs.categories import Category
from mapmyworld.docs.locations import Location


class LocCatReviewed(Schema):
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'reviewed_star': {
            'type': 'integer',
            'format': 'int64',
        },
        'reviewed_title': {
            'type': 'string'
        },
        'reviewed_desc': {
            'type': 'string'
        },
        'reviewed_at': {
            'type': 'date'
        },
        "category": Category,
        "location": Location,
    }
    required = ["id", "reviewed_star", "reviewed_title",
                "reviewed_desc", "reviewed_at", "category", "location"]


class ResponseLocCatReviewed(Schema):
    properties = {
        **ResponseBase.properties,
        'pagination': PaginationResponse,
        'data': LocCatReviewed.array(),
        'total': {
            'type': 'int'
        },
    }


class ResponseNewLocCatReviewed(Schema):
    properties = {
        **ResponseBase.properties,
        'location_category_reviewed': LocCatReviewed,
    }


class ParamsLocCatReviewed(Schema):
    properties = {
        **ParmsPagination.properties,
        'category_id': {
            'type': 'int'
        },
    }


params_pagination = [
    {
        'in': 'query',
        'name': 'pagination and filter',
        'schema': ParamsLocCatReviewed,
        'description': 'pagination data and filter by category_id'
    }]
