class App:
    WINDOW_TITLE: str = "Camera Calibration"

    VIDEO_DIRECTORY: str = "videos"
    VIDEO_FILE: str = "my_video.avi"
    VIDEO_PATH: str = f"{VIDEO_DIRECTORY}/{VIDEO_FILE}"


class ChessBoard:
    PATTERN: tuple[int, int]
    CELL_SIZE: int


class Keycode:
    ESC: int
    SPACE: int
    ENTER: int
