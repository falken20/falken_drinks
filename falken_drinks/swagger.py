from flask_swagger_ui import get_swaggerui_blueprint


print("Loading swagger.py")

# endpoint we want swagger docs to be visible at
SWAGGER_URL = "/swagger"
# json file which contains the endpoints definition for the api
SWAGGER_API_URL = "/static/swagger.json"
# SWAGGER_API_URL = "/static/swagger.yml"


# get_swaggerui_blueprint is used to create a config for the swagger endpoint
# and it is registered within the app using the register_blueprint method (app.py)
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    SWAGGER_API_URL,
    config={
        'app_name': "Falken Plants"
    }
)
