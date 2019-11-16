# Any-Vision-Assignment
Python assignment by Ofekch.
Written in Python 3.7, using Threading module and Flask framework.
##instructions:
- Install requirements file
- Start service by opening command line, and running:
```
cd resize_service
python application.py
```
- Start client test program by opening another command line, and running:
```
cd client
python test_program.py N M PATH_TO_VIDEO
```
Where N is the number of instances to run, M is the time between each instance,
and the last parameter is the path to the video. for example run :
```
cd client
python test_program.py 4 2 './video/example_video.mp4'
```
The results will be in the results folder inside resize_service directory.
