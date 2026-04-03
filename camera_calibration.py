from config import App, ChessBoard, Keycode

import os
import numpy as np
import cv2 as cv


# === States ===
# 부모 추상 클래스
class State:
    controller: CameraCalibration = None

    def __init__(self, controller: CameraCalibration):
        self.controller = controller

    def enter(self):
        print(f"Enter: {type(self).__name__}")
        pass

    def run(self):
        pass

    def exit(self):
        print(f"Exit: {type(self).__name__}")


# 프로그램 시작 상태
class IdleState(State):
    def enter(self):
        super().enter()
        self.controller.set_to_first_frame()

    def run(self):
        self.controller.wait_and_handle_key()

    def exit(self):
        super().exit()


# 동영상 재생 상태
class PlayingState(State):
    def enter(self):
        super().enter()

    def run(self):
        self.controller.read_next_frame()
        self.controller.show_last_frame()
        self.controller.wait_and_handle_key()

    def exit(self):
        super().exit()


# 동영상 정지 상태
class PausedState(State):
    def enter(self):
        super().enter()

    def run(self):
        self.controller.show_last_frame()
        self.controller.wait_and_handle_key()

    def exit(self):
        super().exit()


# 프로그램 종료 상태
class ExitState(State):
    def enter(self):
        super().enter()
        self.controller.exit_program()

    def run(self):
        pass

    def exit(self):
        super().exit()


# === Finite State Machine ===
class FiniteStateMachine:
    current_state: State

    idle_state: IdleState
    playing_state: PlayingState
    paused_state: PausedState
    exit_state: ExitState

    def __init__(self, controller: CameraCalibration):
        self.idle_state = IdleState(controller)
        self.playing_state = PlayingState(controller)
        self.paused_state = PausedState(controller)
        self.exit_state = ExitState(controller)

        self.current_state = self.idle_state

    def run(self):
        if self.current_state is not None:
            self.current_state.run()

    # === Switch State ===
    def switch_state(self, new_state: State):
        if self.current_state is not None:
            self.current_state.exit()
        self.current_state = new_state
        if self.current_state is not None:
            self.current_state.enter()

    def to_idle(self):
        self.switch_state(self.idle_state)

    def to_playing(self):
        self.switch_state(self.playing_state)

    def to_paused(self):
        self.switch_state(self.paused_state)

    def to_exit(self):
        self.switch_state(self.exit_state)

    # === Compare State ===
    def is_state(self, state: State) -> bool:
        return self.current_state is state

    def is_idle(self) -> bool:
        return self.is_state(self.idle_state)

    def is_playing(self) -> bool:
        return self.is_state(self.playing_state)

    def is_paused(self) -> bool:
        return self.is_state(self.paused_state)

    def is_exit(self) -> bool:
        return self.is_state(self.exit_state)


# === Main Program ===
class CameraCalibration:
    # Constant
    WINDOW_TITLE: str = App.CAMERA_CALIBRATION_WINDOW_TITLE
    VIDEO_FILE_PATH: str = App.VIDEO_FILE_PATH

    # Video Data
    video_capture: cv.VideoCapture  # 비디오 캡쳐
    video_height: int  # 비디오 높이
    video_width: int  # 비디오 너비
    video_fps: int  # 비디오 fps
    video_msec: int  # 프레임 간격 (ms)

    # Frame
    last_frame: np.ndarray = None

    # FSM
    state_machine: FiniteStateMachine

    # etc.
    image_list: list[np.ndarray] = []  # 카메라 캘리브레이션 연산에 사용할 이미지 리스트
    camera_calibration_data: dict = {}  # 카메라 캘리브레이션 연산 결과

    # 생성자
    def __init__(self):
        # 비디오 파일 검증
        if self.VIDEO_FILE_PATH == None:
            raise Exception("No Video File Selected")
        if not os.path.isfile(self.VIDEO_FILE_PATH):
            raise Exception("No Video File Exists")
        # 비디오 캡쳐 초기화 및 정보 로드
        self.video_capture = cv.VideoCapture(self.VIDEO_FILE_PATH)
        self._load_video_info()
        # FSM 초기화
        self.state_machine = FiniteStateMachine(self)

    # 비디오 정보 불러오기
    def _load_video_info(self):
        self.video_height = self.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.video_width = self.video_capture.get(cv.CAP_PROP_FRAME_WIDTH)
        self.video_fps = self.video_capture.get(cv.CAP_PROP_FPS)
        self.video_msec = int(1000 / min(self.video_fps, 240))

    # 프로그램 실행
    def run(self):
        self.state_machine.to_playing()

        while not self.state_machine.is_exit():
            self.state_machine.run()

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

    # 다음 프레임 읽기
    def read_next_frame(self):
        valid, frame = self.video_capture.read()

        if not valid:
            self.state_machine.to_idle()
            return

        self.last_frame = frame

    # 마지막 프레임 출력
    def show_last_frame(self):
        if self.last_frame is not None:
            cv.imshow(self.WINDOW_TITLE, self.last_frame)

    # 키 대기 및 처리
    def wait_and_handle_key(self):
        keycode = cv.waitKey(self.video_msec)
        self.handle_key_input(keycode)

    # 비디오 재시작
    def set_to_first_frame(self):
        self.video_capture.set(cv.CAP_PROP_POS_FRAMES, 0)

    # 프로그램 종료
    def exit_program(self):
        self.video_capture.release()
        cv.destroyAllWindows()

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

        # FIXME
        # 해당 부분에서 카메라 캘리브레이션 실패
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

        return True

    # 카메라 캘리브레이션 데이터 출력
    def print_camera_calibration_data(self):
        print("===== Calibration Data =====")
        for key, value in self.camera_calibration_data.items():
            print(f"- {key:<8}:")
            print(f"{value}")
        print("============================")


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
