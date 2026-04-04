from config import App, Keycode
from utils import Json
from base_video_app import BaseVideoApp

import numpy as np
import cv2 as cv


class DistortionCorrection(BaseVideoApp):
    # Constants
    WINDOW_TITLE: str = App.DISTORTION_CORRECTION_WINDOW_TITLE
    VIDEO_FILE_PATH: str = App.VIDEO_FILE_PATH

    # etc.
    is_distortion_correction_enabled: bool = False  # 왜곡 보정 활성화 여부
    camera_matrix: np.ndarray
    distortion_coefficientt: np.ndarray

    # 키 입력 처리
    def handle_key_input(self, keycode: int):
        """
        ESC: 프로그램 종료
        SPACE: 비디오 정지/재생
        ENTER: 왜곡 보정 on/off
        """
        match keycode:
            case Keycode.ESC:  # 프로그램 종료
                self.state_machine.to_exit()
                print("Exit Program.")
            case Keycode.SPACE:  # 비디오 정지/재생
                if self.state_machine.is_idle() or self.state_machine.is_paused():
                    self.state_machine.to_playing()
                elif self.state_machine.is_playing():
                    self.state_machine.to_paused()
            case Keycode.ENTER:  # 왜곡 보정 on/off
                if self.is_distortion_correction_enabled:
                    self.is_distortion_correction_enabled = False
                    print("Disable Distortion Correction")
                else:
                    self.is_distortion_correction_enabled = True
                    print("Enable Distortion Correction")

    # 프로그램 실행
    def run(self):
        self.load_camera_calibration_data()
        super().run()

    # 카메라 캘리브레이션 데이터 불러오기
    def load_camera_calibration_data(self):
        data = Json.load(f"{App.DATA_DIRECTORY}/{App.CAMERA_CALIBRATION_DATA_FILENAME}")
        self.camera_matrix = np.array(data["mtx"])
        self.distortion_coefficientt = np.array(data["dist"])

    # 프레임 가공
    def process_last_frame(self):
        # 원본 프레임 반환
        if not self.is_distortion_correction_enabled:
            return self.last_frame
        # self.frame를 왜곡 보정한 이미지 반환
        mapx, mapy = cv.initUndistortRectifyMap(
            self.camera_matrix,
            self.distortion_coefficientt,
            None,
            None,
            (self.last_frame.shape[1], self.last_frame.shape[0]),
            cv.CV_32F,
        )
        return cv.remap(self.last_frame, mapx, mapy, cv.INTER_LINEAR)
