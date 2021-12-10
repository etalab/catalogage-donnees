from .db import init_db

startup = [
    init_db,
]
