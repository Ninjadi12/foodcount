import os

from flask import Flask, render_template, url_for

picFolder = os.path.join('static', 'pics')



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'showcode.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.config['UPLOAD_FOLDER'] = picFolder
    from . import db
    db.init_app(app)

    from . import auth, carboncalc, user
    app.register_blueprint(auth.bp)
    app.register_blueprint(carboncalc.bp)
    app.register_blueprint(user.bp)

    @app.route('/list')
    def list():

        return render_template('/carboncalc/list.html', title = "Shopping List")

    @app.route('/')
    @app.route('initial')
    def main():
        pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
        return render_template("initial.html", title = "FUCounter", logo = pic1)

    app.add_url_rule('/', endpoint='initial')
    
    return app