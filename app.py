# -*- coding: utf-8 -*-
"""Hawkeye v1.0

Hawkeye is an exercise in building a boilerplate computer vision micro service. It uses Flash and Connexion to provide
web services, and TensorFlow's Object Detection API for... object detection :)
"""

import connexion

import sys
import os
import click
from injector import Module, Injector, singleton
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from services.objectdetector import ObjectDetector


class AppModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder):
        base_path = os.path.dirname(os.path.abspath(__file__))
        detector = ObjectDetector(
            gfpath=self.app.config['model_path'],
            labelpath="{}/object_detection/data/mscoco_label_map.pbtxt".format(base_path)
        )
        binder.bind(ObjectDetector, to=detector, scope=singleton)


@click.command()
@click.option('--port', type=int, required=False, default=9090, help="The port to run on. Default is 9090.")
@click.option('--model_path', type=str, required=True, help="The path to the tensor model 'gffile'.")
def main(port, model_path):
    app = connexion.App(__name__, port=port, specification_dir='swagger/')
    app.add_api('app.yaml', resolver=RestyResolver('api'))

    app.app.config.update(model_path=model_path)
    injector = Injector([AppModule(app.app)])
    FlaskInjector(app=app.app, injector=injector)

    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
