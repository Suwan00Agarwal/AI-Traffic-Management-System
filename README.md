# 🚦 AI-Based Smart Traffic Management System  
### with Emergency Vehicle Priority

---

## 📌 Overview

This project presents a **beginner-level prototype** of an AI-based smart traffic management system that dynamically controls traffic signals based on real-time vehicle density using computer vision.

The system replaces traditional fixed-time traffic signals with an **adaptive signal control mechanism**, improving traffic flow and reducing congestion.

It also includes an **emergency vehicle priority system**, allowing immediate signal clearance for emergency lanes.

---

## 🎯 Problem Statement

Traditional traffic systems use **fixed signal timings**, which leads to:

- Unnecessary waiting time  
- Traffic congestion  
- Inefficient road utilization  
- No priority for emergency vehicles  

This project aims to solve these problems using **AI and real-time decision making**.

---

## 🧠 Key Features

- 🚗 Real-time vehicle detection using YOLOv8  
- 📊 Lane-wise traffic density estimation  
- 🚦 Dynamic signal timing (not fixed)  
- ⚖️ Fair lane selection (avoids starvation)  
- 🚑 Emergency vehicle priority override  
- 🎥 Live video processing using OpenCV  

---

## ⚙️ System Workflow

```text
Video Input (Traffic Camera)
        ↓
Frame Extraction (OpenCV)
        ↓
Vehicle Detection (YOLOv8)
        ↓
Vehicle Classification & Filtering
        ↓
Lane-wise Vehicle Counting
        ↓
Traffic Density Estimation
        ↓
Dynamic Signal Timing Calculation
        ↓
Fair Lane Selection Logic
        ↓
Emergency Override Check
        ↓
Traffic Signal Output (Simulated)
```

## 🛠️ Technologies Used

- Python  
- OpenCV  
- YOLOv8 (Ultralytics)  
- NumPy  
- Git & GitHub  

---

## 🧩 How It Works

1. A traffic video is used as input.  
2. YOLO detects vehicles (cars, bikes, buses, trucks).  
3. Vehicles are assigned to lanes using region-based segmentation.  
4. The number of vehicles in each lane is counted.  

    The system calculates green signal duration dynamically using:
   
    ##  Green Time = Base Time + (Vehicle Count × Time Factor)

6. The lane with the highest traffic gets priority.  
7. A fairness mechanism prevents repeated selection of the same lane.  
8. Emergency mode overrides all logic and gives immediate green signal.  

---

## 🎮 Controls

- Press `1` → Emergency in Lane 1  
- Press `2` → Emergency in Lane 2  
- Press `3` → Emergency in Lane 3  
- Press `4` → Emergency in Lane 4  
- Press `0` → Disable emergency mode  
- Press `q` → Quit  

---

## ⚠️ Important Note (Prototype Disclaimer)

This project is a **beginner-level prototype** and is designed for academic demonstration purposes.

### Simplifications made:

- Uses pre-trained YOLO model (no custom training)  
- Uses vertical lane segmentation (approximation)  
- Uses video input instead of real CCTV feed  
- Simulates traffic signals (no hardware integration)  

---

## ❗ Limitations

- Does not accurately detect ambulances (uses simulated emergency trigger)  
- Lane detection is approximate due to camera perspective  
- No multi-camera or real-time IoT integration  
- Cannot track individual vehicles across frames  
- Performance depends on video quality and angle  

---

## 🚀 Future Improvements

This system can be significantly improved by:

- 🧠 Training a custom model for ambulance detection  
- 📐 Using perspective-based lane detection (polygon regions)  
- 📡 Integrating IoT with real traffic signals  
- 🧮 Using reinforcement learning for optimal signal control  
- 📊 Tracking vehicle movement across frames (object tracking)  
- 🌐 Deploying on edge devices like Raspberry Pi  
- ☁️ Connecting to cloud for smart city integration  

---

## 📈 Potential Applications

- Smart city traffic systems  
- Emergency vehicle routing  
- Urban congestion management  
- Intelligent transportation systems  

---

## 👨‍💻 Author

**Suwan Agarwal**  
Capstone Project – AI Smart Traffic Management System with Emergency Vehicle Priority  

---

## ⭐ Final Note

This project demonstrates how **AI + Computer Vision** can be used to solve real-world problems like traffic congestion and emergency response delays.
While this is a prototype, it provides a strong foundation for building **next-generation intelligent traffic systems**.
