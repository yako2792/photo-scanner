# src/main.py
from packages.webcam_driver import webcam_driver
import cv2

filePath = "test_image.jpg"

def main():
    driver = webcam_driver()
    driver.start()
    
    frame = driver.get_frame()

    cv2.imwrite(filePath, frame)

    driver.release()

    

if __name__ == "__main__":
    main()
