from . import models


def load_models():
    """Import all models to ensure they are registered with SQLAlchemy."""
    return [models.Post]
