from threading import Thread
from uuid import uuid4
from os import mkdir
from time import time
from resizeimage import resizeimage
from io import BytesIO
from PIL import Image


class TaskManager:
    """
    This class handles starting new tasks and threads,
    that will process the images.
    """

    def __init__(self):
        print("Starting task manager")

    def start_new_task(self, images):
        """
        This function gives an id to the task, and starts a thread that will take care of the task.
        :param images: The file dictionary that needs to be processed.
        :return:
        """
        task_id = str(uuid4())
        for image_name in list(images.keys()):
            images[image_name] = images[image_name].read()
        Thread(target=self._resize_video_images, args=(task_id, images)).start()
        print("starting to resize images by task_id -{0}\n".format(task_id))
        return task_id

    def _resize_video_images(self, task_id, images):
        """
        creates a directory for the results of task,
        starts a thread for each image to process them concurrently,
        waits until they finish and prints how long it took.
        """
        mkdir("./results/task_id--{0}".format(task_id))
        threads = list()
        start_time = time()
        for image_name in list(images.keys()):
            t = Thread(target=self._resize_image, args=(images[image_name], image_name, task_id))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        end_time = time()
        print("all images have finished processing for task_id -{0}\n"
              "time for instance - {1}"
              .format(task_id, str(end_time - start_time)))

    @staticmethod
    def _resize_image(image, image_name, task_id):
        """
        Resize an image and saves it to disk.
        """
        new_image = Image.open(BytesIO(image))
        new_image = resizeimage.resize_cover(new_image, [400, 200])
        new_image.save('./results/task_id--{0}/new_{1}'.format(task_id, image_name.split('/')[-1]), "JPEG")
