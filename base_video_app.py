from config import App

import os
import numpy as np
import cv2 as cv


# === States ===
# 부모 추상 클래스
class State:
    controller: BaseVideoApp = None

    def __init__(self, controller: BaseVideoApp):
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

    def __init__(self, controller: BaseVideoApp):
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


# 비디오 가공 후 출력 및 키 입력을 처리하는 프로그램의 추상 클래스
class BaseVideoApp:
    # Constant
    WINDOW_TITLE: str
    VIDEO_FILE_PATH: str

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
        pass

    # === Actions ===

    # 다음 프레임 읽기
    def read_next_frame(self):
        valid, frame = self.video_capture.read()

        if not valid:
            # self.state_machine.to_exit()
            self.state_machine.to_idle()
            return

        self.last_frame = frame

    # 프레임 가공
    def process_last_frame(self):
        return self.last_frame

    # 마지막 프레임 출력
    def show_last_frame(self):
        if self.last_frame is not None:
            cv.imshow(self.WINDOW_TITLE, self.process_last_frame())

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
