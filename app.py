from flask import Flask, render_template, Response
import cv2


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen_from_cam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imwrite("test.jpg", frame)
        f = open("test.jpg", 'rb').read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + f + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_from_cam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
