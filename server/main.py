import sys

from .api.app import create_app
from .config.di import bootstrap
from .infrastructure.server import run

bootstrap()

app = create_app()

if __name__ == "__main__":
    sys.exit(run("server.main:app"))
