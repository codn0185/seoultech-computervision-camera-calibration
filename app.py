from camera_calibration import CameraCalibration
from distortion_correction import DistortionCorrection


def main():
    while True:
        print("\n\n")
        print("===== Select Option =====")
        print("0: Exit Program")
        print("1: Camera Calibration")
        print("2: Distortion Correction")
        print("=========================")
        option = int(input("Option:"))

        match (option):
            case 0:
                print("Program Exited")
                break
            case 1:
                print("Program Running: Camera Calibration")
                app = CameraCalibration()
                app.run()
            case 2:
                print("Program Running: Distortion Correction")
                app = DistortionCorrection()
                app.run()
            case _:
                print(f"Invalid Option Selected: {option}")


if __name__ == "__main__":
    main()
