from flask_restful import Resource, reqparse
from mapmyworld.utils import api_response as Response
from mapmyworld.utils import exceptions, messages
from mapmyworld.models import locations
from mapmyworld.extensions import db
from werkzeug.exceptions import BadRequest
import math
from flask_restful_swagger_3 import swagger
from mapmyworld.docs import locations as lc, schemas


class RestLocation(Resource):
    _args = reqparse.RequestParser(bundle_errors=True)
    _args.add_argument("limit", type=int, location="args")
    _args.add_argument("page", type=int, location="args")

    _json = reqparse.RequestParser(bundle_errors=True)
    _json.add_argument("longitude", type=float, location="json", required=True, help="Longitude is required")
    _json.add_argument("latitude", type=float, location="json", required=True, help="Longitude is required")

    @swagger.tags(['Locations'])
    @swagger.response(response_code=200, description="Successful operation", summary="List Locations", schema=lc.ResponseLocations)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    @swagger.response(response_code=204, description="No content")
    @swagger.parameters(params=schemas.params_pagination)
    def get(self):
        try:
            args = self._args.parse_args()
            limit = args.get("limit", 0)
            page = args.get("page", 0)

            query = db.session.query(locations.Location).filter_by(
                register_status=True
            )
            total_items = query.count()
            if total_items == 0:
                return Response.generic_not_content_response()

            total_pages = 1
            if limit > 0:
                offset = page * limit
                total_pages = math.ceil(total_items / limit)
                query = query.offset(offset).limit(limit)

            results = query.all()
            schema = locations.LocationSchema(many=True)
            results = schema.dump(results)
            resp_data = dict(
                data=results,
                total=len(results),
                pagination=dict(
                    total_items=total_items,
                    total_pages=total_pages,
                    current_page=page
                )
            )
            return Response.generic_response(resp_data, messages.SUCCESFUL_RESPONSE)
        except Exception as e:
            return exceptions.handle_exception(e)

    @swagger.tags(['Locations'])
    @swagger.reqparser(name='AddLocation', parser=_json)
    @swagger.response(response_code=201, description="Successful operation", summary="Register location", schema=lc.ResponseNewLocation)
    @swagger.response(response_code=400, description="Bad Request", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=422, description="Validation Error", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    def post(self):
        try:
            args = self._json.parse_args()
            longitude = args.get("longitude", None)
            latitude = args.get("latitude", None)

            if not latitude or latitude < -90 or latitude > 90:
                error = dict(latitude="Latitude must be between -90 and 90.")
                return Response.generic_error_response(errors=error)
            if not longitude or longitude < -180 or longitude > 180:
                error = dict(
                    latitude="Longitude must be between -180 and 180.")
                return Response.generic_error_response(errors=error)

            location = db.session.query(locations.Location).filter_by(
                latitude=latitude,
                longitude=longitude,
            ).first()

            message_ok = messages.CREATED_SUCCESFUL_RESPONSE
            if location and location.register_status:
                return Response.generic_error_response(message=f"Location is already registered.", code=422)

            if not location:
                location = locations.Location(
                    latitude=latitude,
                    longitude=longitude,
                    user_id=1,
                )
                db.session.add(location)
                db.session.flush()

            else:
                message_ok = "Location Already existed and was reactivated"
                location.register_status = True

            schema = locations.LocationSerializer()
            location = schema.dump(location)
            resp = dict(location=location)
            db.session.commit()
            return Response.generic_response(resp, message_ok)
        except BadRequest as ebad:
            errors = ebad.data.get("message")
            return Response.generic_error_response(errors=errors)
        except Exception as e:
            return exceptions.handle_exception(e)


