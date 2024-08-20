# packages/webcam_driver.py
import cv2
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
        self.cap = None

    def start(self):
        """
        Opens webcam and configure video capture.
        
        :raises: Exception if device could not be opened.
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        if (not self.cap.isOpened()):
            raise Exception("Could not open video device")
        
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
    
    def get_frame(self):
        """
        Capture one frame.

        :return: Captured frame.
        c
        """
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
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