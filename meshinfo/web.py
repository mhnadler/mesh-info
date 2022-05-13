"""Main entry point for the Pyramid web application."""

from __future__ import annotations

from gunicorn.app.base import BaseApplication  # type: ignore
from pyramid.config import Configurator

from .config import AppConfig


class GunicornApplication(BaseApplication):
    """Run pyMeshMap WSGI application via Gunicorn.

    Based on the "Custom Application" in the Gunicorn docs.

    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """Set configuration options based on the passed settings."""
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main(config: Configurator, settings: AppConfig.Web, *, reload: bool = False):
    """Create and run the Pyramid WSGI application."""

    GunicornApplication(
        config.make_wsgi_app(),
        {
            "bind": settings.bind,
            "workers": settings.workers,
            "reload": reload,
        },
    ).run()
