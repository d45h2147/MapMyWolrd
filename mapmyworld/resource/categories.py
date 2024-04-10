from flask_restful import Resource, reqparse
from mapmyworld.utils import api_response as Response
from mapmyworld.utils import exceptions, messages
from mapmyworld.models import categories
from mapmyworld.extensions import db
from werkzeug.exceptions import BadRequest
from flask_restful_swagger_3 import swagger
from mapmyworld.docs import categories as ct, schemas  
import math


class RestCategories(Resource):
    params = reqparse.RequestParser()
    params.add_argument("name", type=str, location="json",required=True, help="name is required")

    _args = reqparse.RequestParser()
    _args.add_argument("limit", type=int, default=0, required=False, location="args")
    _args.add_argument("page", type=int, default=0, required=False, location="args")

    @swagger.tags(['Categories'])
    @swagger.response(response_code=200, description="Successful operation", summary="List category", schema=ct.ResponseCategories)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    @swagger.response(response_code=204, description="No content")
    @swagger.parameters(params=schemas.params_pagination)
    def get(self):
        try:
            args = self._args.parse_args()
            limit = args.get("limit", 0)
            page = args.get("page", 0)

            query = db.session.query(categories.Category).filter_by(
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
            schema = categories.CategorySchema(many=True)
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

    @swagger.tags(['Categories'])
    @swagger.reqparser(name='AddCategory', parser=params)
    @swagger.response(response_code=201, description="Successful operation", summary="Register category", schema=ct.ResponseNewCategory)
    @swagger.response(response_code=400, description="Bad Request", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=422, description="Validation Error", schema=schemas.ResponseBadRequest)
    @swagger.response(response_code=500, description="Internal Server Error", schema=schemas.ResponseBase)
    def post(self):
        """
        Crea una nueva categoría o reactiva una existente inactiva.
        """
        try:
            args = self.params.parse_args()
            name = args.get("name", None)

            if not name:
                error = dict(name="Name is required.")
                return Response.generic_error_response(errors=error)

            category = db.session.query(categories.Category).filter_by(
                name=name
            ).first()

            message_ok = messages.CREATED_SUCCESFUL_RESPONSE
            if category and category.register_status:
                return Response.generic_error_response(message=f"category ({name}) is already registered.", code=422)

            if not category:
                category = categories.Category(
                    name=name,
                    user_id=1,
                )
                db.session.add(category)
                db.session.flush()
            else:
                message_ok = "Category Already existed and was reactivated"
                category.register_status = True

            schema = categories.CategorySerializer()
            category = schema.dump(category)
            resp = dict(category=category)
            db.session.commit()
            return Response.generic_response(resp, message_ok, 201)
        except BadRequest as ebad:
            errors = ebad.data.get("message")
            return Response.generic_error_response(errors=errors)
        except Exception as e:
            return exceptions.handle_exception(e)
