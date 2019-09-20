# Hawkeye

Hawkeye is an exercise in building a computer vision micro service. It provides web services through [Flask](http://flask.pocoo.org/) and [connexion](https://github.com/zalando/connexion), and object detection though [TensorFlow](https://www.tensorflow.org) (more specifically TF's [object detection API](https://github.com/tensorflow/models/tree/master/research/object_detection)).

## Requirements

Python `3.7`

## Setup

* Download a pre-trained model from the [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) (or BYOM)
* Unzip the model in the project folder
* `pip install -r requirements.txt`
* Run `app.py`

## Command Line Arguments

| Flag          | Type         | Required  |  Description                                                  |
|---------------|--------------|-----------|---------------------------------------------------------------|
| `--help`      |              |           | Prints the list of command line arguments                     |
| `--port`      | `Integer`    | No        | The port on which the service should run. Default is 9090     |
| `--model_path`| `String`     | Yes       | The path to your model.pb file                                |

## Docker

Build the docker container:

```bash
docker build -t hawkeye .
```

Run the container like so:

```bash
docker run -p 9090:9090 \
           -v $(pwd)/tensor_models:/tensor_models \
          hawkeye --model_path /tensor_models/frozen_inference_graph.pb
```

## Detecting Objects

Make a multipart `POST` request to `/v1/images` and pass an image in the `file` parameter.

### Request Parameters

| Name          | Type         | Required  |  Description                                                  |
|---------------|--------------|-----------|---------------------------------------------------------------|
| `file`        | `image/jpeg` | Yes       | The image you wish to scan of objects                         |
| `limit`       | `Integer`    | No        | The max number of detected objects to return (default: `100`) |
| `confidence`  | `Float`      | No        | The min confidence of objects to return (default: `0.0`)      |

### Sample Response

The response object contains the dimensions of the original image along with the bounding box, confidence rating and name of each detected object.

```json
{
  "image": {
    "filename": "city.jpg",
    "height": 1920,
    "width": 1080
  },
  "objects": [
    {
      "bounds": {
        "max_x": 0.9026010036468506,
        "max_y": 0.7274996042251587,
        "min_x": 0.8731642961502075,
        "min_y": 0.6027235984802246
      },
      "confidence": 0.899111807346344,
      "name": "person"
    },
    {
      "bounds": {
        "max_x": 0.4548061490058899,
        "max_y": 0.7350420355796814,
        "min_x": 0.30975914001464844,
        "min_y": 0.6559353470802307
      },
      "confidence": 0.8316138982772827,
      "name": "car"
    },
    {
      "bounds": {
        "max_x": 0.6277451515197754,
        "max_y": 0.7549415826797485,
        "min_x": 0.4210185706615448,
        "min_y": 0.6356408596038818
      },
      "confidence": 0.7929925918579102,
      "name": "car"
    },
  ],
  "uid": "7c287660-c46e-4d21-93fb-6e2414a4795d"
}
```

Please note that the the bounding boxes are defined as relative values rater than pixel offsets.

This allows you to send lower resolution versions of images to the detection API and then easily translate the bounding boxes in the response back to your high resolution source image. Simply multiply the `x` positions in the response by the `width`, and the `y` positions by the `height` of your source image.

# Swagger

Swagger UI can be accessed via `/v1/ui`

# License

MIT
