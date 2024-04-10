from mapmyworld.docs.schemas import Schema, ResponseBase, PaginationResponse


class Location(Schema):
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'latitude': {
            'type': 'float'
        },
        'longitude': {
            'type': 'float'
        },
    }
    required = ['name']


class ResponseNewLocation(Schema):
    properties = {
        **ResponseBase.properties,
        'location': Location,
    }


class ResponseLocations(Schema):
    properties = {
        **ResponseBase.properties,
        'pagination': PaginationResponse,
        'data': Location.array(),
        'total': {
            'type': 'int'
        },
    }
