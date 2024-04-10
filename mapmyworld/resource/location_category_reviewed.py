from flask_restful import Resource, reqparse
from mapmyworld.utils import api_response as Response
from mapmyworld.utils import exceptions, messages
from mapmyworld.models import location_category_reviewed, locations, categories
from mapmyworld.extensions import db
from werkzeug.exceptions import BadRequest
from flask_restful import Resource
import math
from flask_restful_swagger_3 import swagger
from mapmyworld.docs import location_category_reviewed as lcr, schemas


class RestLocationCategoryReviewed(Resource):
    _args = reqparse.RequestParser(bundle_errors=True)
    _args.add_argument("category_id", type=int, location="args")
    _args.add_argument("limit", type=int, default=0, location="args")
    _args.add_argument("page", type=int, default=0, location="args")

    _json = reqparse.RequestParser(bundle_errors=True)
    _json.add_argument("location_id", type=int, location="json",
                       required=True, help="Location_id is required.")
    _json.add_argument("category_id", type=int, location="json",
                       required=True, help="Category_id is required.")
    _json.add_argument("reviewed_star", type=int, location="json",
                       required=True, help="Reviewed_star is required.")
    _json.add_argument("reviewed_title", type=str, location="json",
                       required=True, help="Reviewed_title is required.")
    _json.add_argument("reviewed_desc", type=str, location="json",
                       required=True, help="Reviewed_desc is required.")

    @swagger.tags(['Location Category Reviewed'])
    @swagger.response(response_code=200, description="Successful operation", summary="List Location Category Reviewed", schema=lcr.ResponseLocCatReviewed)
    @swagger.response(response_code=400, description="Bad Request", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    @swagger.response(response_code=204, description="No content")
    @swagger.parameters(params=lcr.params_pagination)
    def get(self):
        try:
            args = self._args.parse_args()
            category = args.get("category_id", None)
            limit = args.get("limit", 0)
            page = args.get("page", 0)

            query = db.session.query(
                location_category_reviewed.LocationCategoryReviewed,
            ).join(
                locations.Location
            ).join(
                categories.Category
            ).filter(
                location_category_reviewed.LocationCategoryReviewed.register_status == True
            )

            if category:
                query = query.filter(categories.Category.id == category)

            total_items = query.count()
            if total_items == 0:
                return Response.generic_response(code=204)

            total_pages = 1
            if limit > 0:
                offset = page * limit
                total_pages = math.ceil(total_items / limit)
                query = query.offset(offset).limit(limit)

            results = query.all()
            schema = location_category_reviewed.LocationCategoryReviewedSchema(
                many=True)
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
        except BadRequest as ebad:
            errors = ebad.data.get("message")
            return Response.generic_error_response(errors=errors)
        except Exception as e:
            return exceptions.handle_exception(e)

    @swagger.tags(['Location Category Reviewed'])
    @swagger.reqparser(name='AddLocationCategoryReviewed', parser=_json)
    @swagger.response(response_code=201, description="Successful operation", summary="Register LocationCategoryReviewed", schema=lcr.ResponseNewLocCatReviewed)
    @swagger.response(response_code=400, description="Bad Request", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=422, description="Validation Error", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    def post(self):
        try:
            args = self._json.parse_args()
            location_id = args.get("location_id", None)
            category_id = args.get("category_id", None)
            reviewed_star = args.get("reviewed_star", None)
            reviewed_title = args.get("reviewed_title", None)
            reviewed_desc = args.get("reviewed_desc", None)

            if not location_id:
                error = dict(location_id="location_id is required")
                return Response.generic_error_response(errors=error)

            if not category_id:
                error = dict(category_id="category_id is required")
                return Response.generic_error_response(errors=error)

            if not (reviewed_star >= 1 and reviewed_star <= 5):
                error = dict(
                    reviewed_star="reviewed_star must be between 1 and 5")
                return Response.generic_error_response(errors=error)

            if not reviewed_title:
                error = dict(reviewed_title="reviewed_title is required")
                return Response.generic_error_response(errors=error)

            if not reviewed_desc:
                error = dict(reviewed_desc="reviewed_desc is required")
                return Response.generic_error_response(errors=error)

            reviewed = db.session.query(
                location_category_reviewed.LocationCategoryReviewed
            ).filter_by(
                category_id=category_id,
                location_id=location_id,
            ).first()

            message_ok = messages.CREATED_SUCCESFUL_RESPONSE
            if reviewed and reviewed.register_status:
                message_warning = f"Location Category Reviewed is already registered"
                return Response.generic_error_response(message=message_warning, code=422)

            if not reviewed:
                reviewed = location_category_reviewed.LocationCategoryReviewed(
                    location_id=location_id,
                    category_id=category_id,
                    reviewed_star=reviewed_star,
                    reviewed_title=reviewed_title,
                    reviewed_desc=reviewed_desc,
                    user_id=1,
                )
                db.session.add(reviewed)
                db.session.flush()
            else:
                message_ok = "Location Category Reviewed Already existed and was reactivated"
                reviewed.register_status = True

            schema = location_category_reviewed.LocationCategoryReviewedSchema()
            reviewed = schema.dump(reviewed)
            resp = dict(location_category_reviewed=reviewed)
            db.session.commit()
            return Response.generic_response(resp, message_ok)
        except BadRequest as ebad:
            errors = ebad.data.get("message")
            return Response.generic_error_response(errors=errors)
        except Exception as e:
            return exceptions.handle_exception(e)
