import sys
import argparse
import cv2
import json


class Light360:
    def __init__(self, min_thresh=150, max_thresh=255):
        self.min_thresh = min_thresh
        self.max_thresh = max_thresh

    # 最も明るい領域の中心を探す
    # (x座標, y座標), 輝度(0～255)
    def __find_brightest_region_center(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 明るさのしきい値
        _, thresh = cv2.threshold(
            gray, self.min_thresh, self.max_thresh, cv2.THRESH_BINARY
        )
        # 閾値に応じた輪郭抽出
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None, None

        # 最も大きい輪郭を探す
        largest_contour = max(contours, key=cv2.contourArea)

        # 最も大きい輪郭の中心
        moments = cv2.moments(largest_contour)
        if moments["m00"] == 0:
            return None, None
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        return (cx, cy), gray[cy, cx]

    # ピクセル座標を球座標に変換
    def __pixel_to_spherical(self, x, y, width, height):
        lon = (x / width) * 360.0 - 180.0  # Longitude in degrees
        lat = 90.0 - (y / height) * 180.0  # Latitude in degrees
        return lon, lat

    def __analysis_frame(self, frame_id, frame):
        height, width = frame.shape[:2]
        center, brightness = self.__find_brightest_region_center(frame)
        if center:
            x, y = center
            lon, lat = self.__pixel_to_spherical(x, y, width, height)
            # print(f"{frame_id},{x},{y},{brightness},{lon},{lat}")
            return {
                "frameID": frame_id,
                "x": x,
                "y": y,
                "lon": lon,
                "lat": lat,
                "brightness": int(brightness),
            }
        else:
            print(f"Frame {frame_id}: No bright regions detected.")
            return None

    def analysis(self, video_path):
        # Create a VideoCapture object
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open video file.")
            return
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        total_duration = total_frames / fps

        results = {
            "fps": fps,
            "totalFrames": total_frames,
            "totalDuration": total_duration,
            "frameInfo": [],
        }

        frame_id = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results["frameInfo"].append(self.__analysis_frame(frame_id, frame))
            frame_id += 1

        cap.release()
        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="360deg video to light coordinate.")
    parser.add_argument("-i", "--video", required=True, help="Input 360deg Video file")
    parser.add_argument("-o", "--json", help="Output JSON (optional)")
    args = parser.parse_args()

    light360 = Light360()
    result = light360.analysis(args.video)

    if args.json:
        with open(args.json, "w") as jf:
            jf.write(json.dumps(result))
    else:
        sys.stdout.write(json.dumps(result))
