from mapmyworld.extensions import db, ma, cors, api
from flask import render_template, send_from_directory


def configure_app(app):
    db.init_app(app)
    ma.init_app(app)
    api.init_app(app)
    cors.init_app(app)

    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        db.session.remove()

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/swagger')
    def swagger_ui():
        return send_from_directory('static/swagger-ui', 'index.html')

    return app
