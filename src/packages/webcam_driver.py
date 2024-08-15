# packages/webcam_driver.py
import cv2

class webcam_driver:
    def __init__(self, camera_index=0):
        """
        Initialize webcam driver with webcam index.
        :param camera_index: Camera index (Vale 0 by default).
        """
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        """
        Opens webcam and configure video capture.
        
        :raises: Exception if device could not be opened.
        """
        self.cap = cv2.VideoCapture(self.camera_index)
        if (not self.cap.isOpened()):
            raise Exception("Could not open video device")
    
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