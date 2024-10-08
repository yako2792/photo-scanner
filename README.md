# Webcam Interface with Qt and OpenCV

This project provides a user interface to view connected webcams, adjust image settings, and save photos at regular intervals. It also includes Arduino communication for specific control tasks.

## Requirements

- **Python** (3.x)
- **Qt** (for the graphical interface)
- **OpenCV** (for image processing)
- **Virtualenv** (for managing the virtual environment)
- **PySerial** (for Arduino communication)

## Installation

1. Clone repository
    ```bash
    git clone https://github.com/yako2792/photo-scanner.git
    cd photo-scanner
    ```

2. Activate local virtual env
    - Windows
    ```bash
    .\local-env\Scripts\activate
    ```
    - Linux/MacOS
    ```bash
    source .\local-env\bin\activate
    ```

3. Verify dependencies are installed
    ```bash
    pip install -r requirements.txt
    ```

## How to run

1. Ensure virtual env is activated.

2. Ensure arduino is connected via  ```COM7```.
    > **NOTE:** If arduino is not in ```COM7```, it can be modified in ```packages.window_driver.py```.

3. Execute application.
    ```bash
    python .\src\main.py
    ```

## Project Structure

    ├───.vscode
    ├───local-env
    │   ├───Lib
    │   │   └───site-packages
    │   │       ├───cv2
    │   │       ├───numpy
    │   │       ├───pip
    │   │       └───...
    ├───packages
    │   ├───__init__.py
    │   ├───WindowDriver.py
    │   ├───camera_DRIVER.py
    │   └───...
    ├───main.py
    ├───requirements.txt
    └───README.md
    
## Features

* Real-time visualization of three cameras (cameras should not be connected using same USB Hub).
* Adjustment of image parameters such as brightness, contrast, etc.
* Capture of images at defined intervals.
* Export of captured images.