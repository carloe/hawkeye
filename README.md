# Hawkeye

Hawkeye is an exercise in building a computer vision micro service. It provides web services through [Flask](http://flask.pocoo.org/) and [connexion](https://github.com/zalando/connexion), and object detection though [TensorFlow](https://www.tensorflow.org) (more specifically TF's [object detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)).

## Requirements

Python `3.6`

## Setup

* Download a pre-trained model from the [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) (or BYOM)
* Unzip the model in the project folder
* Open `app.py` and point `gfpath` to your model
* `pip install -r requirements.txt`
* Run `app.py`

## Detecting Objects

Make a multipart `POST` request to `/v1/images` and pass an image in the `file` parameter to see what happens :)

### Request Parameters

| Name          | Type         | Required  |  Description                                                  |
|---------------|--------------|-----------|---------------------------------------------------------------|
| `file`        | `image/jpeg` | Yes       | The image you wish to scan of objects                         |
| `limit`       | `Integer`    | No        | The max number of detected objects to return (default: `100`) |
| `confidence`  | `Float`      | No        | The min confidence of objects to return (default: `0.0`)      |

# Swagger

Swagger UI can be accessed via `/v1/ui`

# License

MIT
