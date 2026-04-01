from camera_calibration import CameraCalibration
from distortion_correction import DistortionCorrection


def main():
    option = int(
        input(
            """
            === Select Option ===
            1: Camera Calibration
            2: Distortion Correction
            =====================
            """
        )
    )

    match (option):
        case 1:
            print("Running Camera Calibration")
            app = CameraCalibration()
            app.run()
        case 2:
            print("Running Distortion Correction")
            app = DistortionCorrection()
            app.run()
        case _:
            print(f"Invalid Option Selected: {option}")


if __name__ == "__main__":
    main()
