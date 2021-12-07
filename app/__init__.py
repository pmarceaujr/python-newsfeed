from flask import Flask
from app.routes import home

def create_app(test_config=None):
  # set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )
  @app.route('/hello')
  def hello():
    return 'hello world, this is my first REST route with PYTHON!'
  return app

  ## Lesson 1 Set up FLASK: CREATE THE HOME VIEW ROUTES!