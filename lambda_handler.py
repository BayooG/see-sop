from mangum import Mangum
from service.main import app

lambda_handler = Mangum(app, lifespan="off")
