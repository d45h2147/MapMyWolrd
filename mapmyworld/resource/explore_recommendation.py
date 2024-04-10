from flask_restful import Resource, reqparse
from mapmyworld.utils import api_response as Response
from mapmyworld.utils import exceptions, messages
from mapmyworld.models import location_category_reviewed, locations, categories
from mapmyworld.extensions import db
from werkzeug.exceptions import BadRequest
from datetime import datetime, timedelta
from flask_restful import Resource
from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, types
from sqlalchemy.sql.expression import literal
import math
from mapmyworld.docs import explore_recommendation as rec, schemas  
from flask_restful_swagger_3 import swagger


class RestExploreRecommendation(Resource):
    _args = reqparse.RequestParser(bundle_errors=True)
    _args.add_argument("limit", type=int, default=10, location="args")
    _args.add_argument("page", type=int, default=0, location="args")
    _args.add_argument("category_id", type=int, location="args")

    @swagger.tags(['Explore Recommendation'])
    @swagger.response(response_code=200, description="Successful operation", summary="List category", schema=rec.ResponseRecommendation)
    @swagger.response(response_code=400, description="Internal Server Error", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    @swagger.response(response_code=204, description="No content")
    @swagger.parameters(params=rec.params_pagination)
    def get(self):
        try:
            args = self._args.parse_args()
            category = args.get("category_id", None)
            limit = args.get("limit", 10)
            page = args.get("page", 0)
            offset = page * limit

            if not limit:
                error = dict(limit="The limit must be greater than zero.")
                return Response.generic_error_response(errors=error)

            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            recent_reviews_subquery = db.session.query(
                (location_category_reviewed.LocationCategoryReviewed.location_id.cast(types.String)+'-' +
                 location_category_reviewed.LocationCategoryReviewed.category_id.cast(types.String)).label("recent_review_key")
            ).filter(
                location_category_reviewed.LocationCategoryReviewed.register_status == True,
                location_category_reviewed.LocationCategoryReviewed.reviewed_at >= thirty_days_ago
            ).subquery()

            query = db.session.query(
                categories.Category.id.label("category_id"),
                categories.Category.name.label("category_name"),
                locations.Location.id.label("location_id"),
                locations.Location.longitude,
                locations.Location.latitude,
            ).join(
                categories.Category, literal(True)
            ).outerjoin(
                location_category_reviewed.LocationCategoryReviewed,
                and_(categories.Category.id == location_category_reviewed.LocationCategoryReviewed.category_id,
                     locations.Location.id == location_category_reviewed.LocationCategoryReviewed.location_id)
            ).filter(
                categories.Category.register_status == True,
                locations.Location.register_status == True,
                    (locations.Location.id.cast(types.String)+'-' +
                     categories.Category.id.cast(types.String)).notin_(recent_reviews_subquery)
            ).order_by(
                location_category_reviewed.LocationCategoryReviewed.reviewed_at
            )
            if category:
                query = query.filter(categories.Category.id == category)

            total_items = query.count()
            results = query.offset(offset).limit(limit).all()

            if len(results) == 0:
                return Response.generic_not_content_response()

            results = [{
                'category_id': row.category_id,
                'category_name': row.category_name,
                'location_id': row.location_id,
                'longitude': str(row.longitude),
                'latitude': str(row.latitude)
            } for row in results]

            total_pages = math.ceil(total_items / limit)
            resp_data = dict(
                data=results,
                total=len(results),
                pagination=dict(
                    total_items=total_items,
                    total_pages=total_pages,
                    current_page=page
                )
            )
            return Response.generic_response(resp_data, message=messages.SUCCESFUL_RESPONSE)
        except BadRequest as ebad:
            errors = ebad.data.get("message")
            return Response.generic_error_response(errors=errors)
        except Exception as e:
            return exceptions.handle_exception(e)
