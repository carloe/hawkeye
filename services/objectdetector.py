# -*- coding: utf-8 -*-
"""This module handles object detection through TensorFlow"""

from __future__ import print_function

import uuid
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

NUM_CLASSES = 90
IMAGE_SIZE = (12, 8)


class ObjectDetector(object):
    __detection_graph = None
    __category_index = None

    def __init__(self, gfpath: str, labelpath: str):
        self.__detection_graph = tf.Graph()
        with self.__detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(gfpath, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(labelpath)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        self.__category_index = label_map_util.create_category_index(categories)

    def __load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def scan(self, image, outputDebugImage=False) -> dict:
        result = []

        with self.__detection_graph.as_default():
            with tf.Session(graph=self.__detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = self.__detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = self.__detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = self.__detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = self.__detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = self.__detection_graph.get_tensor_by_name('num_detections:0')

                # the array based representation of the image will be used later in order to prepare the
                # result image with boxes and labels on it.
                image_np = self.__load_image_into_numpy_array(image)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections], feed_dict={image_tensor: image_np_expanded})

                for i in range(0, scores.size):
                    score = float(scores[0][i])
                    clsid = classes[0][i]
                    name = self.__category_index[clsid]['name']
                    box = boxes[0][i]

                    if score > 0.8:
                        print(box)

                    obj = {
                        "name": name,
                        "confidence": score,
                        "bounds": {
                            "min_y": float(box[0]),
                            "min_x": float(box[1]),
                            "max_y": float(box[2]),
                            "max_x": float(box[3]),
                        }
                    }
                    result.append(obj)

                if outputDebugImage == True:
                    # Visualization of the results for debugging.
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        self.__category_index,
                        use_normalized_coordinates=True,
                        line_thickness=8)
                    plt.figure(figsize=IMAGE_SIZE)
                    im = Image.fromarray(image_np)
                    imagepath = "/tmp/{}.jpg".format(str(uuid.uuid4()))
                    im.save(imagepath)
                    print("Debug image saved to: {}".format(imagepath))

        return result
