"""API Gateway HTTP API と Lambda の接続アダプター。"""

from mangum import Mangum

from app.main import app

handler = Mangum(app, lifespan="off")
