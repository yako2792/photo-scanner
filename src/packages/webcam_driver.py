# packages/webcam_driver.py
import cv2
import time
import numpy as np
from PyQt5.QtGui import QImage, QPixmap

class webcam_driver:
    def __init__(self, camera_index=0, width=1920, height=1080):
        """
        Initialize webcam driver with webcam index.
        :param camera_index: Camera index (Vale 0 by default).
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height

        self.min_zoom = None;
        self.max_zoom = None;

        # Video proc options
        self.default_brightness = 0
        self.default_contrast = 1
        self.default_saturation = 1
        self.default_hue_shift = 0

        self.brightness = self.default_brightness
        self.contrast = self.default_contrast
        self.saturation = self.default_saturation
        self.hue_shift = self.default_hue_shift

        # Camera video options
        self.default_exposure = -6
        self.default_gain = 0

        self.exposure = self.default_exposure
        self.gain = self.default_gain


        self.cap = None

    def start(self):
        """
        Opens webcam and configure video capture.
        
        :raises: Exception if device could not be opened.
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        if (not self.cap.isOpened()):
            raise Exception("Could not open video device")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        print(f"[Camera {self.camera_index}] Resolution set ({self.width} x {self.height}).")
        self.characterize_camera()

        # Initialize first frames
        self.get_frame()
        time.sleep(0.1)
        self.get_frame()
        time.sleep(0.1)
        self.get_frame()
        time.sleep(0.1)

    
    def get_frame(self):
        """
        Capture one frame.

        :return: Captured frame.
        """
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = self.apply_adjustments(frame)
                return frame
            else:
                raise Exception("Failed to grab frame")
        else:
            raise Exception("Camera not started")
    
    def to_pixmap(self, frame):
        """
        Convert the OpenCV frame to QPixmap.

        :param frame: Frame captured from the camera.
        :return: QPixmap of the captured frame.
        """

        # Convert frame BGR to RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get shape of frame
        height, width, channels = rgb_image.shape

        # Create the QImage
        q_image = QImage(rgb_image.data, width, height, channels * width, QImage.Format_RGB888)
        
        # Return converted image
        return QPixmap.fromImage(q_image)
    
    def is_zoom_enabled(self):
        """
        Check if camera has zoom options
        """
        current_zoom = self.cap.get(cv2.CAP_PROP_ZOOM)
        return current_zoom != -1
    
    def set_gain(self, gain_value):
        """
        Apply given zoom to camera.
        :param zoom_value: Zoom value to be applied.
        """
        self.gain = gain_value

    def set_brightness(self, value):
        """
        Set a brightness value.
        :param value: Value to be set.
        """
        self.brightness = value

    def set_contrast(self, value):
        """
        Set a contrast value.
        :param value: Value to be set.
        """
        self.contrast = value

    def set_saturation(self, value):
        """
        Set a saturation value.
        :param value: Value to be set.
        """
        self.saturation = value

    def set_hue_shift(self, value):
        """
        Set a HUE value.
        :param value: Value to be set.
        """
        self.hue_shift = value


    def apply_adjustments(self, frame):
        """
        Apply all adjustments in picture
        :param frame: Frame were settings will be applied.
        """
        # Adjust exposure
        self.cap.set(cv2.CAP_PROP_EXPOSURE, self.exposure)

        # Adjust gain/iso
        self.cap.set(cv2.CAP_PROP_GAIN, self.gain)

        # Adjust brightness
        frame = cv2.add(frame, np.array([self.brightness, self.brightness, self.brightness], dtype=np.uint8))

        # Adjust contrast
        frame = cv2.convertScaleAbs(frame, alpha=self.contrast, beta=0)

        # Adjust saturation
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], self.saturation)
        
        # Adjust matrix
        hsv[:, :, 0] = (hsv[:, :, 0] + self.hue_shift) % 180

        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return frame

    def characterize_camera(self):
        """
        Characterize camera values/properties
        """
        # Get min and max zoom values
        zoom_values = []
        if self.is_zoom_enabled():
            for zoom_value in range(1, 11):
                success = self.cap.set(cv2.CAP_PROP_ZOOM, zoom_value)
                if success:
                    zoom_values.append(zoom_value)
            
            if zoom_values:
                self.min_zoom = min(zoom_values)
                self.max_zoom = max(zoom_values)  
            else:
                print(f"[Camera {self.camera_index}] No zoom values were successfully set.")  
        else:
            print(f"[Camera {self.camera_index}] Camera has no zoom values.")

        
    def set_exposure(self, value):
        """
        Set camera exposure manually.
        :param value: New exposure value.
        """
        self.exposure = value

    def release(self):
        """
        Release camera resources.

        Call this method after using cam.
        """
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __del__(self):
        """
        Ensure camera releases after object destruction.
        """
        self.release()