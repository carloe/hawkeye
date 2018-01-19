# -*- coding: utf-8 -*-
""" This module provides the /images route of the service """

from __future__ import print_function

import uuid
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage
from flask_injector import inject
from services.objectdetector import ObjectDetector


@inject(detector=ObjectDetector)
def post(detector: ObjectDetector, file: FileStorage) -> dict:
    uid = str(uuid.uuid4())

    image = Image.open(BytesIO(file.stream.read()))
    objects = detector.scan(image)

    width, height = image.size

    result = {
        'uid': uid,
        'image': {
            'filename': file.filename,
            'width': width,
            'height': height
        },
        'objects': objects
    }

    return result, 200
