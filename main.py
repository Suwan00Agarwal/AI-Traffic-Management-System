import cv2
import time
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")

# Vehicle classes to count
vehicle_classes = ["car", "motorcycle", "bus", "truck"]

# Video path
video_path = "videos/traffic.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Signal timing settings
BASE_TIME = 5
TIME_PER_VEHICLE = 2
MIN_GREEN_TIME = 5
MAX_GREEN_TIME = 30

# Signal state variables
current_green_lane = None
green_start_time = None
green_duration = 0

# Emergency state
emergency_mode = False
emergency_lane = None

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_height, frame_width, _ = frame.shape
    lane_width = frame_width // 4

    lane_counts = {
        "Lane 1": 0,
        "Lane 2": 0,
        "Lane 3": 0,
        "Lane 4": 0
    }

    # Run YOLO
    results = model(frame)[0]

    # Draw lane boundaries
    cv2.line(frame, (lane_width, 0), (lane_width, frame_height), (255, 0, 0), 2)
    cv2.line(frame, (2 * lane_width, 0), (2 * lane_width, frame_height), (255, 0, 0), 2)
    cv2.line(frame, (3 * lane_width, 0), (3 * lane_width, frame_height), (255, 0, 0), 2)

    # Detect and count vehicles lane-wise
    for box in results.boxes:
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]

        if class_name in vehicle_classes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            if center_x < lane_width:
                lane_name = "Lane 1"
            elif center_x < 2 * lane_width:
                lane_name = "Lane 2"
            elif center_x < 3 * lane_width:
                lane_name = "Lane 3"
            else:
                lane_name = "Lane 4"

            lane_counts[lane_name] += 1

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)

            cv2.putText(
                frame,
                f"{class_name} - {lane_name}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    current_time = time.time()

    # Emergency override logic
    if emergency_mode and emergency_lane is not None:
        current_green_lane = emergency_lane
        remaining_time = "EMERGENCY"
    else:
        # Normal dynamic timing logic
        if current_green_lane is None or (current_time - green_start_time) >= green_duration:
            # Exclude last green lane if possible
            candidate_lanes = {k: v for k, v in lane_counts.items() if k != current_green_lane}

            if any(count > 0 for count in candidate_lanes.values()):
                next_lane = max(candidate_lanes, key=candidate_lanes.get)
            else:
                next_lane = max(lane_counts, key=lane_counts.get)

            current_green_lane = next_lane

            vehicle_count = lane_counts[current_green_lane]

            calculated_time = BASE_TIME + (vehicle_count * TIME_PER_VEHICLE)
            green_duration = max(MIN_GREEN_TIME, min(calculated_time, MAX_GREEN_TIME))

            green_start_time = current_time

        remaining_time = int(green_duration - (current_time - green_start_time))
        if remaining_time < 0:
            remaining_time = 0

    # ---------------- UI SECTION ----------------

    # Title
    cv2.putText(
        frame,
        "AI Smart Traffic Management System",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    # Lane Counts
    cv2.putText(frame, "Lane Density:", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

    y_offset = 100
    for lane, count in lane_counts.items():
        cv2.putText(
            frame,
            f"{lane}: {count}",
            (20, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )
        y_offset += 25

    # Signal Status
    cv2.putText(frame, "Signal Status:", (20, y_offset + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

    signal_y = y_offset + 50
    for lane in lane_counts.keys():
        if lane == current_green_lane:
            status = "GREEN"
            color = (0, 255, 0)
            thickness = 3
        else:
            status = "RED"
            color = (0, 0, 255)
            thickness = 2

        cv2.putText(
            frame,
            f"{lane}: {status}",
            (20, signal_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            thickness
        )
        signal_y += 25

    # Current Active Lane
    cv2.putText(
        frame,
        f"Active Lane: {current_green_lane}",
        (20, signal_y + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # Timer
    cv2.putText(
        frame,
        f"Timer: {remaining_time}",
        (20, signal_y + 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    # Emergency Mode Highlight
    if emergency_mode:
        cv2.putText(
            frame,
            "EMERGENCY MODE ACTIVE",
            (400, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 165, 255),
            3
        )

    cv2.imshow("Smart Traffic Control with Emergency Priority", frame)

    key = cv2.waitKey(25) & 0xFF

    # Press 1/2/3/4 to trigger emergency lane
    if key == ord('1'):
        emergency_mode = True
        emergency_lane = "Lane 1"
    elif key == ord('2'):
        emergency_mode = True
        emergency_lane = "Lane 2"
    elif key == ord('3'):
        emergency_mode = True
        emergency_lane = "Lane 3"
    elif key == ord('4'):
        emergency_mode = True
        emergency_lane = "Lane 4"
    # Press 0 to disable emergency mode
    elif key == ord('0'):
        emergency_mode = False
        emergency_lane = None
        current_green_lane = None
        green_start_time = None
        green_duration = 0
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()