from config import App, ChessBoard, Keycode
from video_processing import VideoProcessing

import os
import numpy as np
import cv2 as cv


class DistortionCorrection(VideoProcessing):
    WINDOW_TITLE: str = App.DISTORTION_CORRECTION_WINDOW_TITLE
    VIDEO_FILE_PATH: str = App.DISTORTION_CORRECTION_VIDEO_FILE_PATH

    # 프레임 가공
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        pass

    # 키 입력 처리
    def handle_key_input(self, keycode: int, frame: np.ndarray = None):
        match keycode:
            case Keycode.ESC:
                pass
            case Keycode.ENTER:
                pass
            case Keycode.SPACE:
                pass
        """
        ESC: 프로그램 종료
        ENTER: 왜곡 보정 on/off
        SPACE: 정보 출력 (로그)
        """
