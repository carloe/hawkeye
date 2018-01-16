# -*- coding: utf-8 -*-
"""Hawkeye v1.0

Hawkeye is an exercise in building a boilerplate computer vision micro service. It uses Flash and Connexion to provide
web services, and TensorFlow's Object Detection API for... object detection :)
"""

import connexion

import os
from injector import Binder
from flask_injector import FlaskInjector
from connexion.resolver import RestyResolver

from services.objectdetector import ObjectDetector


def configure(binder: Binder) -> Binder:
    basepath = os.path.dirname(os.path.abspath(__file__))
    binder.bind(ObjectDetector, ObjectDetector(
        # Path to the tensorflow model gffile
        gfpath="{}/tensor_models/ssd_inception_v2_coco_2017_11_17/frozen_inference_graph.pb".format(basepath),
        # Path to the tensorflow object_detection API labels
        labelpath="{}/object_detection/data/mscoco_label_map.pbtxt".format(basepath)
    ))
    return binder


if __name__ == '__main__':
    app = connexion.App(__name__, port=9090, specification_dir='swagger/')
    app.add_api('app.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run()
