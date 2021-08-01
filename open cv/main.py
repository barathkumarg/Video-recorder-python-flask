from flask import Flask, render_template, Response,send_file
import cv2
import datetime
import os
app = Flask(__name__)






#setting the camera, width and size
camera = cv2.VideoCapture(0)
frame_width = int(camera .get(3))
frame_height = int(camera .get(4))

size = (frame_width, frame_height)

#creating the instance for the video capturing to save

filename='recorded_outputs/output'
file_name = f'{filename}.avi'
result = cv2.VideoWriter(file_name ,
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         20,size)

#function to get the frames to stream in webpage and store it in file
def generate_frames():
    while True:

        ## read the camera frame
        success, frame = camera.read()

        if not success:
            break
        else:

            ret, buffer = cv2.imencode('.jpg', frame)
            result.write(frame)
            frame = buffer.tobytes()



        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



# url routes to navigate pages
#render the first html page
@app.route('/')
def index():
    return render_template('index.html')


#calling the video function to stream video in webpage
@app.route('/video')
def video():

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#function finish recording and saving it
@app.route('/finished',methods=['POST','GET'])
def finished():
    camera.release()
    result.release()
    cv2.destroyAllWindows()
    return render_template('success.html')


#function to download the video of the recording
@app.route('/download',methods=['post','get'])
def download():
    return send_file(file_name, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)
