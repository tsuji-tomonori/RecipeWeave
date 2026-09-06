"""API Gateway HTTP API / Lambda adapter."""

from mangum import Mangum

from app.main import app

handler = Mangum(app, lifespan="off")
