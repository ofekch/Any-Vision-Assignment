from flask import Flask, request, jsonify
from resize_service.task_manager import TaskManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
task_manager = TaskManager()


@app.route('/resize_images', methods=['POST'])
def resize_video_images():
    pictures_to_resize = request.files.to_dict()
    result = task_manager.start_new_task(pictures_to_resize)
    return jsonify({"task_id": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
