class App:
    VIDEO_DIRECTORY: str = "videos"

    CAMERA_CALIBRATION_WINDOW_TITLE: str = "Camera Calibration"
    CAMERA_CALIBRATION_VIDEO_FILE_NAME: str = "my_video_1.avi"
    CAMERA_CALIBRATION_VIDEO_FILE_PATH: str = (
        f"{VIDEO_DIRECTORY}/{CAMERA_CALIBRATION_VIDEO_FILE_NAME}"
    )

    DISTORTION_CORRECTION_WINDOW_TITLE: str = "Distortion Correction"
    DISTORTION_CORRECTION_VIDEO_FILE_NAME: str = "my_video_2.avi"
    DISTORTION_CORRECTION_VIDEO_FILE_PATH: str = (
        f"{VIDEO_DIRECTORY}/{DISTORTION_CORRECTION_VIDEO_FILE_NAME}"
    )


class ChessBoard:
    PATTERN: tuple[int, int]
    CELL_SIZE: int


class Keycode:
    ESC: int = 27
    SPACE: int = 32
    ENTER: int = 13
