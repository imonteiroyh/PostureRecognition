import cv2
import time
import pose_module as pm


capture = cv2.VideoCapture('video.mp4')
detector = pm.PoseDetector()

frame_count = 0
previous_time = 0
while True:
    frame_read_sucess, frame = capture.read()

    if not frame_read_sucess:
        break

    frame = detector.get_pose(frame)
    landmarks = detector.get_position(frame)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("c"):
        cv2.imwrite(f"frame_{frame_count}.png", frame)
        frame_count += 1

cv2.destroyAllWindows()