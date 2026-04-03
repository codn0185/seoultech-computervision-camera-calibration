import os


class App:
    VIDEO_DIRECTORY: str = "video"
    VIDEO_FILENAME: str = "my_video.mp4"
    VIDEO_FILE_PATH: str = os.path.join(VIDEO_DIRECTORY, VIDEO_FILENAME)

    CAMERA_CALIBRATION_WINDOW_TITLE: str = "Camera Calibration"
    DISTORTION_CORRECTION_WINDOW_TITLE: str = "Distortion Correction"


class ChessBoard:
    PATTERN: tuple[int, int] = (7, 10)  # Vertices (h, w)
    CELL_SIZE: int = 25  # Cell Size (mm)


class Keycode:
    ESC: int = 27
    SPACE: int = 32
    ENTER: int = 13
    A: int = 65
    a: int = 97
    R: int = 82
    r: int = 114
