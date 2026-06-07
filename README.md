# Autonomous Multi Terrain RASP Rover Navigation PyBullet

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyBullet](https://img.shields.io/badge/PyBullet-Robotics-orange)
![Path Planning](https://img.shields.io/badge/A*-Algorithm-green)

## Overview

This project presents an autonomous terrain-aware rover navigation system developed in PyBullet. The rover traverses multiple terrain types while avoiding obstacles using the A* path planning algorithm.

The simulation demonstrates important robotics concepts including:

- Path Planning
- Obstacle Avoidance
- Terrain-Aware Navigation
- Autonomous Mobility
- Robotics Simulation

The project is inspired by the RASP Rover platform and serves as a digital testbed for autonomous navigation algorithms.

---

## Features

- A* Path Planning

- Obstacle Avoidance

- Multi-Terrain Navigation

- Smooth Terrain Traversal

- Rough Terrain Traversal

- Slope Climbing

- Terrain-Aware Speed Adaptation

- 4-Wheel Rover Simulation

- PyBullet Physics Environment

---

## System Architecture

```text
Environment
     ↓
Terrain Analysis
     ↓
Localization
     ↓
A* Path Planner
     ↓
Waypoint Generation
     ↓
Motion Controller
     ↓
Rover Navigation
```

---

## Terrain Types

### Smooth Terrain

Represents flat tiled surfaces where the rover can travel at higher speeds.

### Rough Terrain

Represents uneven ground that requires slower traversal.

### Slope Terrain

Represents inclined terrain requiring controlled ascent.

---

## Path Planning

The rover uses the A* search algorithm to determine an optimal path from the start position to the goal position.

The evaluation function is:

f(n) = g(n) + h(n)

Where:

- g(n) = Actual cost from start node
- h(n) = Heuristic estimate to goal
- f(n) = Total estimated cost

Euclidean Distance is used as the heuristic function.

---

## Simulation Environment

The environment contains:

- Multiple terrain zones
- Static obstacles
- Start position
- Goal position
- Planned path visualization

---

## Demo

The simulation demonstrates autonomous navigation of a 4-wheel rover across multiple terrain types using A* path planning.

### Demonstrated Features

- Generation of an optimal path using A* search
- Obstacle avoidance in a grid-based environment
- Terrain-aware navigation across:
  - Smooth terrain
  - Rough terrain
  - Sloped terrain
- Adaptive traversal speed based on terrain conditions
- Goal-directed autonomous navigation

### Simulation Demo

![Demo](demo/MR Simulation.gif)


---

## Results

The rover successfully:

- Avoids obstacles
- Generates collision-free paths
- Traverses multiple terrain types
- Reaches the target location autonomously

---

## Technologies Used

- Python
- PyBullet
- NumPy
- Robotics Algorithms
- A* Path Planning

---

## Future Work

- SLAM Integration
- IMU-Based Localization
- Camera-Based Obstacle Detection
- ROS2 Integration
- RRT* Path Planning Comparison
- Real Hardware Deployment on RASP Rover

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Autonomous-Terrain-Aware-Rover-Navigation.git
cd Autonomous-Terrain-Aware-Rover-Navigation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python src/main.py
```

---

## Author

Ananya

Mechanical Engineering | Robotics | Autonomous Systems

