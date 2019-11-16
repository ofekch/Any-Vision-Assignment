from time import sleep
import sys
from requests import post
import cv2
from PIL import Image
import numpy

# Loading parameters from command line arguments.
N, M, PATH_TO_VIDEO = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]


def split_video_to_images():
    """
    This function splits the given video from the command-line path to frames,
    and will return a dictionary that contains every frame in this way:
    key = frame_number
    value = image_file bytes
    """

    print("splitting video to frames")
    video = cv2.VideoCapture(PATH_TO_VIDEO)
    images = dict()
    success, image = video.read()
    frame_number = 1
    while success:
        image = Image.fromarray(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR), 'RGB').save(
            './frames/frame{0}.jpeg'.format(frame_number), 'JPEG')
        image_file = open('./frames/frame{0}.jpeg'.format(frame_number), 'rb')
        images[image_file.name] = image_file.read()
        success, image = video.read()
        frame_number += 1
    return images


def send_tasks_to_server(n, m):
    """
    :param n: number of instances
    :param m: number of seconds to wait before every instance
    This function invokes the split video function, and then sends N instances to the server,
    with M seconds in between every request.
    """
    image_files = split_video_to_images()
    for i in range(0, n):
        send_resize_video_request(files=image_files, instance=i)
        sleep(m)


def send_resize_video_request(files, instance):
    result = post(url='http://localhost:5000/resize_images', files=files).json()
    print("task_id {0} for instance {1}".format(result["task_id"], instance))


if __name__ == '__main__':
    send_tasks_to_server(N, M)
