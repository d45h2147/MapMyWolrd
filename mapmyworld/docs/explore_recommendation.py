from mapmyworld.docs.schemas import Schema, ResponseBase, PaginationResponse, ParmsPagination


class Recommendation(Schema):
    properties = {
        'category_id': {
            'type': 'integer',
            'format': 'int64',
        },
        'location_id': {
            'type': 'integer',
            'format': 'int64',
        },
        'category_name': {
            'type': 'string'
        },
        'latitude': {
            'type': 'string'
        },
        'longitude': {
            'type': 'string'
        },

    }
    required = ["category_id", "category_name",
                "latitude", "location_id", "longitude"]


class ResponseRecommendation(Schema):
    properties = {
        **ResponseBase.properties,
        'pagination': PaginationResponse,
        'data': Recommendation.array(),
        'total': {
            'type': 'int'
        },
    }


class ParamsRecommendation(Schema):
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
        'schema': ParamsRecommendation,
        'description': 'pagination data and filter by category_id'
    }]
