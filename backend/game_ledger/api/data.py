from game_ledger import context
from werkzeug.exceptions import *
from flask import Blueprint, request, send_file
from flask.views import MethodView
from game_ledger.resources.data import Data
import flask, io


class DataApi(MethodView):
    def get(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        requested_data_id = request.args.get("id")
        if not requested_data_id:
            raise BadRequest()

        requested_data = Data.get_by_id(context.get_db_connection(), requested_data_id)

        response = send_file(
            io.BytesIO(requested_data.content), mimetype=requested_data.mime_type
        )
        return response

    def post(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        mime_type = request.headers.get("Content-Type")
        if mime_type is None:
            raise BadRequest()

        data = Data.create(
            context.get_db_connection(),
            user=current_user,
            content=request.get_data(),
            mime_type=mime_type,
        )
        return flask.jsonify({"id": data.id})

    def delete(self):
        current_user = context.get_current_user()
        if current_user is None:
            raise Unauthorized()
        requested_data_id = request.args.get("id")
        Data.delete(
            context.get_db_connection(), user=current_user, id=requested_data_id
        )
        return ""


data_blueprint = Blueprint("data", __name__, url_prefix="data/")
data_blueprint.add_url_rule("/", view_func=DataApi.as_view("data"))
