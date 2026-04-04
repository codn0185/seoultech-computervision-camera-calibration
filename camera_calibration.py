from config import App, ChessBoard, Keycode
from utils import Json
from base_video_app import BaseVideoApp

import os
import numpy as np
import cv2 as cv


# 체스보드를 촬영한 동영상을 사용하여 카메라 캘리브레이션을 수행하는 프로그램
class CameraCalibration(BaseVideoApp):
    # Constant
    WINDOW_TITLE: str = App.CAMERA_CALIBRATION_WINDOW_TITLE
    VIDEO_FILE_PATH: str = App.VIDEO_FILE_PATH

    # etc.
    image_list: list[np.ndarray] = []  # 카메라 캘리브레이션 연산에 사용할 이미지 리스트
    camera_calibration_data: dict = {}  # 카메라 캘리브레이션 연산 결과

    # 키 입력 처리
    def handle_key_input(self, keycode: int):
        """
        ESC: 프로그램 종료
        SPACE: 비디오 정지/재생
        ENTER: 카메라 캘리브레이션 연산 및 결과 출력
        A/a: 이미지 리스트에 현재 프레임 추가
        R/r: 이미지 리스트 초기화
        """
        match keycode:
            # 프로그램 종료
            case Keycode.ESC:
                self.state_machine.to_exit()
                print("Exit Program.")
            # 비디오 정지/재생
            case Keycode.SPACE:
                if self.state_machine.is_idle() or self.state_machine.is_paused():
                    self.state_machine.to_playing()
                elif self.state_machine.is_playing():
                    self.state_machine.to_paused()
            # 카메라 캘리브레이션 연산 및 결과 출력
            case Keycode.ENTER:
                if self.calibrate_camera_and_save_result():
                    print("Camera calibration succeeded.")
                    self.print_camera_calibration_data()
                else:
                    print("Failed to perform camera calibration.")
            # 이미지 리스트에 현재 프레임 추가
            case Keycode.A | Keycode.a:
                self.add_last_frame_to_image_list()
                print(
                    f"Added current frame to the image list. (size: {len(self.image_list)})"
                )
            # 이미지 리스트 초기화
            case Keycode.R | Keycode.r:
                self.clear_image_list()
                print("Cleared the image list.")

    # === Actions ===

    # 현재 프레임을 이미지 리스트에 추가
    def add_last_frame_to_image_list(self):
        if self.last_frame is not None:
            self.image_list.append(self.last_frame.copy())

    # 이미지 리스트 초기화
    def clear_image_list(self):
        self.image_list.clear()

    # 카메라 캘리브레이션 연산 및 성공 여부 반환
    def calibrate_camera_and_save_result(self) -> bool:
        if len(self.image_list) < 10:  # 최소 10장 이상일 때 안정적
            print("Camera calibration requires at least 10 images.")
            return False

        img_points = []
        for image in self.image_list:
            gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            complete, pts = cv.findChessboardCorners(gray, ChessBoard.PATTERN)
            if complete:
                img_points.append(pts)

        if not img_points:
            print(
                "No complete chessboard corners were detected in the selected images."
            )
            return False

        obj_pts = [
            [c, r, 0]
            for r in range(ChessBoard.PATTERN[1])
            for c in range(ChessBoard.PATTERN[0])
        ]
        obj_points = [np.array(obj_pts, dtype=np.float32) * ChessBoard.CELL_SIZE] * len(
            img_points
        )

        # 카메라 캘리브레이션
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
            obj_points, img_points, gray.shape[::-1], None, None
        )

        self.camera_calibration_data = {
            "mtx": mtx,  # Camera Matrix - K
            "dist": dist,  # Distortion Coefficient - d
            "rvecs": rvecs,  # Rotation Matrix - R
            "tvecs": tvecs,  # Transform Matrix - t
        }

        # .json 파일로 저장
        self.save_camera_calibration_data_to_json()

        return True

    # 카메라 캘리브레이션 데이터 출력
    def print_camera_calibration_data(self):
        print("===== Calibration Data =====")
        for key, value in self.camera_calibration_data.items():
            print(f"- {key:<8}:")
            print(f"{value}")
        print("============================")

    # 카메라 캘리브레이션 데이터를 json 파일로 저장
    def save_camera_calibration_data_to_json(self):
        Json.save(
            self.camera_calibration_data,
            f"{App.DATA_DIRECTORY}/{App.CAMERA_CALIBRATION_DATA_FILENAME}",
        )


""" 
IDLE (프로그램 시작 / 비디오 종료)
    프로그램 시작 시 자동으로 PLAYING 상태 전환
    SPACE 키 입력 시 재생

PLAYING (비디오 재생)
    SPACE 키 입력 시 PAUSED 상태 전환
    비디오 재생 종료 시 IDLE 상태 전환
    
PAUSED (비디오 정지)
    SPACE 키 입력 시 PLAYING 상태 전환
    
EXIT (프로그램 종료)
    아무 상태에서 ESC 키 입력 시 EXIT 상태 전환
"""


""" 
TODO: 임시 동영상 설정 후 작동 테스트
"""
