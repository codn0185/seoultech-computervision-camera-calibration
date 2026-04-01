import os
import numpy as np
import cv2 as cv


# 비디오 가공 후 출력 및 키 입력을 처리하는 프로그램의 추상 클래스
class VideoProcessing:
    WINDOW_TITLE: str
    VIDEO_FILE_PATH: str

    # === 비디오 ===
    video: cv.VideoCapture  # 비디오 캡쳐
    video_height: int  # 비디오 높이
    video_width: int  # 비디오 너비
    video_fps: int  # 비디오 fps
    video_msec: int  # 프레임 간격 (ms)

    # 비디오 파일 검증 및 비디오 캡쳐 초기화
    def __init__(self):
        if self.VIDEO_FILE_PATH == None:
            raise Exception("No Video File Selected")
        if not os.path.isfile(self.VIDEO_FILE_PATH):
            raise Exception("No Video File Exists")

        self.video = cv.VideoCapture(self.VIDEO_FILE_PATH)

    # 비디오 정보 불러오기
    def _load_video_info(self):
        self.video_height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.video_width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.video_fps = self.video.get(cv.CAP_PROP_FPS)
        self.video_msec = int(1000 / min(self.video_fps, 360))

    # 프로그램 실행
    def run(self):
        self._loop()

    # 프레임 처리 및 키 입력 처리 루프
    def _loop(self):
        valid, frame = self.video.imread()

        # 비디오 재생 불가 시 종료
        if not valid:
            return

        # 키 입력 처리
        self.handle_key_input(cv.waitKey(0), frame)

        # 프레임 가공
        processed_frame = self.process_frame(frame)

        # 화면에 가공된 프레임 출력
        cv.imshow(self.WINDOW_TITLE, processed_frame)

        # 반복
        self._loop()

    # 프레임 가공
    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        pass

    # 키 입력 처리
    def handle_key_input(self, keycode: int, frame: np.ndarray = None):
        pass
