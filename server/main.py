from .api.app import create_app
from .config.di import bootstrap

bootstrap()

app = create_app()
