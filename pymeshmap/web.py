"""Main entry point for the Pyramid web application."""

import hupper
import waitress
from pyramid.config import Configurator

from .config import AppConfig, Environment


def main(
    app_config: AppConfig, *, host: str = "", port: int = None, reload: bool = False
):
    """Create and run the Pyramid WSGI application."""

    if reload:
        reloader = hupper.start_reloader("pymeshmap.cli.main")
        reloader.watch_files([".env"])

    app = make_wsgi_app(app_config)

    host = host or app_config.web.host
    port = port or app_config.web.port

    waitress.serve(app, host=host, port=port)


def make_wsgi_app(app_config: AppConfig):
    """Create the Pyramid WSGI application"""

    settings = {"app_config": app_config}

    # TODO: add development checks, etc
    if app_config.env == Environment.PROD:
        settings["pyramid.reload_templates"] = False
        settings["pyramid.debug_authorization"] = False
        settings["pyramid.debug_notfound"] = False
        settings["pyramid.debug_routematch"] = False
        settings["pyramid.default_locale_name"] = "en"
    elif app_config.env == Environment.DEV:
        settings["pyramid.reload_templates"] = True
        settings["pyramid.debug_authorization"] = False
        settings["pyramid.debug_notfound"] = False
        settings["pyramid.debug_routematch"] = False
        settings["pyramid.default_locale_name"] = "en"

    with Configurator(settings=settings) as config:
        config.include("pyramid_mako")
        config.include("pyramid_services")
        config.include(".routes")
        config.include(".models")

        if app_config.env == Environment.DEV:
            config.include("pyramid_debugtoolbar")

        config.scan()

    return config.make_wsgi_app()
