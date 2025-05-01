import cv2
import numpy as np
import argparse
from Focuser import Focuser

focuser = None

def focusing(val):
    focuser.set(Focuser.OPT_FOCUS, val)

def laplacian(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (320, 180))
    lap = cv2.Laplacian(small, cv2.CV_16U)
    return cv2.mean(lap)[0]

def gstreamer_pipeline(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=30, flip_method=2):
    return (
        "nvarguscamerasrc ! "
        f"video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, format=NV12, framerate={framerate}/1 ! "
        f"nvvidconv flip-method={flip_method} ! "
        f"video/x-raw, width={display_width}, height={display_height}, format=BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=BGR ! appsink"
    )

def show_camera():
    max_index = 10
    max_value = 0.0
    last_value = 0.0
    dec_count = 0
    focal_distance = 10
    focus_finished = False
    skip_frame = 2

    cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    if not cap.isOpened():
        print("Unable to open camera")
        return

    cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
    focusing(focal_distance)

    while cv2.getWindowProperty("CSI Camera", 0) >= 0:
        ret, img = cap.read()
        if not ret:
            break

        cv2.imshow("CSI Camera", img)

        if skip_frame == 0:
            skip_frame = 3
            if dec_count < 6 and focal_distance < 1000:
                focusing(focal_distance)
                sharpness = laplacian(img)

                if sharpness > max_value:
                    max_index = focal_distance
                    max_value = sharpness

                if sharpness < last_value:
                    dec_count += 1
                else:
                    dec_count = 0

                if dec_count < 6:
                    last_value = sharpness
                    focal_distance += 10
            elif not focus_finished:
                focusing(max_index)
                focus_finished = True
        else:
            skip_frame -= 1

        key = cv2.waitKey(16) & 0xFF
        if key == 27:
            break
        elif key == 10:
            max_index = 10
            max_value = 0.0
            last_value = 0.0
            dec_count = 0
            focal_distance = 10
            focus_finished = False

    cap.release()
    cv2.destroyAllWindows()

def parse_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--i2c-bus', type=int, required=True,
                        help='I2C bus number (e.g., 9 for CAM1 on Jetson Orin Nano)')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_cmdline()
    focuser = Focuser(args.i2c_bus)
    show_camera()