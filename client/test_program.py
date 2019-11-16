from time import sleep
import sys
from requests import post
import cv2
from PIL import Image
import numpy


N, M, PATH_TO_VIDEO = sys.argv[1], sys.argv[2], sys.argv[3]
print(N,M,PATH_TO_VIDEO)

def split_video_to_images():
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


def send_tasks_to_server(N, M):
    image_files = split_video_to_images()
    for i in range(0, N):
        send_resize_video_request(image_files, i)
        sleep(M)


def send_resize_video_request(files, i):
    result = post(url='http://localhost:5000/resize_images', files=files).json()
    print("task_id {0} for instance {1}".format(result["task_id"], i))


if __name__ == '__main__':
    send_tasks_to_server(7, 0)
