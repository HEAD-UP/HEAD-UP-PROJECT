# 1. Import libraries
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import json
import time
import socket

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from utils import label_map_util
from utils import visualization_utils as vis_util

if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
sys.path.append("..")

# 1-1. Set Camera ID
camera_id = 1

# 2. Set ML model
MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')
NUM_CLASSES = 90

# 3. Load model into Memory
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

# 4. Load label-map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# 5. Read initial line point
f = open("output_stream.txt", 'r')
f_data = f.read()
f.close()
f_data = f_data.split()

a = float(f_data[0])
b = float(f_data[1])
c = float(f_data[2])

# 6. Declare object tracking function and warning signal function
def get_distance_from_line(x1, y1, a, b, c):
    return (a*x1 + b*y1 + c) / (((a ** 2) + (b ** 2)) ** 0.5)

standard_distance = 0.03
def get_warning_signal(input_distance, input_class):
    if standard_distance > input_distance:
        if input_class == 'person':
            return 0
        else:
            return 1
    return -1

# 7. Set socket environment
HOST = '20.20.0.101'
PORT = 8990
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 8. Object tracking from streaming video
cap = cv2.VideoCapture(0)
signal = -1
time_signal = -1
time_value = time.time()

with detection_graph.as_default():
    with tf.compat.v1.Session(graph=detection_graph) as sess:
        ret = True
        while (ret):
            ret, image_np = cap.read()
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8)

            for index, value in enumerate(classes[0]):
                ymin = boxes[0][index][0]
                xmin = boxes[0][index][1]
                ymax = boxes[0][index][2]
                xmax = boxes[0][index][3]
                class_name = (category_index.get(value)).get('name')
                widthvalue = int((xmax - xmin) / 2)  # width length
                heightvalue = int((ymax - ymin) / 2)  # height length
                if ((class_name == "person" or class_name == "car") and scores[0, index] > 0.80):
                    get_distance_from_line((xmin + xmax) / 2, (ymin + ymax) / 2, a, b, c)
                    signal = get_warning_signal(
                        get_distance_from_line((xmin + xmax) / 2, (ymin + ymax) / 2, a, b, c), class_name)
                    if signal >= 0:
                        if (signal >= time_signal):
                            time_signal = signal
                            time_value = time.time()

            if (time.time() - time_value < 1):
                signal = time_signal
            else:
                time_signal = -1
                time_value = 0

            Camera_data = {
                'Camera_ID': camera_id,
                'Value': signal
            }

            message = json.dumps(Camera_data) + "\n"
            client_socket.sendall(message.encode())
            signal = -1

            # waitKey(value down -> more CPU)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            data = client_socket.recv(1024)

        cv2.destroyAllWindows()
        cap.release()

client_socket.close()