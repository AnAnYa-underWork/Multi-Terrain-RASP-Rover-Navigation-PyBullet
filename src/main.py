import pybullet as p
import pybullet_data
import time
import math
import heapq
import random

# =========================================================
# CONNECT
# =========================================================

p.connect(p.GUI)
p.resetSimulation()

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)

# =========================================================
# CAMERA
# =========================================================

p.resetDebugVisualizerCamera(
    cameraDistance=40,
    cameraYaw=58,
    cameraPitch=-40,
    cameraTargetPosition=[22, -8, 2]
)

# =========================================================
# GROUND
# =========================================================

plane = p.loadURDF("plane.urdf")

# =========================================================
# HELPER FUNCTION
# =========================================================

def create_box(position, size, color):

    visual = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=size,
        rgbaColor=color
    )

    collision = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=size
    )

    body = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=collision,
        baseVisualShapeIndex=visual,
        basePosition=position
    )

    return body

# =========================================================
# TERRAIN HEIGHT FUNCTION
# =========================================================

def get_height(x):

    # Flat regions
    if x < 24:
        return 0.1

    # Slope region
    else:
        return 0.1 + ((x - 24) * 0.06)

# =========================================================
# SMOOTH TERRAIN
# =========================================================

smooth_terrain = create_box(
    position=[6,-8,0.05],
    size=[8,10,0.05],
    color=[0.95,0.95,0.95,1]
)

# =========================================================
# TILE EFFECT
# =========================================================

for x in range(-2,9):

    p.addUserDebugLine(
        [x,-18,0.11],
        [x,2,0.11],
        [0.75,0.75,0.75],
        lineWidth=1
    )

for y in range(-18,2):

    p.addUserDebugLine(
        [-2,y,0.11],
        [9,y,0.11],
        [0.75,0.75,0.75],
        lineWidth=1
    )

# =========================================================
# ROUGH TERRAIN
# =========================================================

rough_terrain = create_box(
    position=[18,-8,0.06],
    size=[8,10,0.06],
    color=[0.55,0.38,0.2,1]
)

# =========================================================
# ROCKY EFFECT
# =========================================================

for _ in range(120):

    rock_x = random.uniform(11,25)
    rock_y = random.uniform(-16,0)

    rock_size = random.uniform(0.03,0.09)

    create_box(
        position=[rock_x,rock_y,0.12],
        size=[rock_size,rock_size,rock_size],
        color=[0.35,0.25,0.15,1]
    )

# =========================================================
# SOLID SLOPE USING SEGMENTS
# =========================================================

slope_start_x = 24

segment_length = 1.5
segment_height = 0.06

num_segments = 14

for i in range(num_segments):

    x = slope_start_x + i * segment_length

    top_z = 0.1 + i * segment_height

    block_height = top_z / 2 + 0.08

    create_box(
        position=[x,-8,block_height],
        size=[segment_length/2 + 0.05,10,block_height],
        color=[0.2,0.65,0.2,1]
    )

# =========================================================
# ROVER
# =========================================================

robot = p.loadURDF(
    "husky/husky.urdf",
    [0,0,0.3]
)

# =========================================================
# GRID MAP
# =========================================================

grid = [

[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],

[0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],

[0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0],

[0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0],

[0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0],

[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0],

[0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],

[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

]

ROWS = len(grid)
COLS = len(grid[0])

start = (0,0)
goal = (7,17)

# =========================================================
# CREATE OBSTACLES
# =========================================================

for r in range(ROWS):

    for c in range(COLS):

        if grid[r][c] == 1:

            x = c * 2.5
            y = -r * 2

            terrain_z = get_height(x)

            obstacle_visual = p.createVisualShape(
                p.GEOM_BOX,
                halfExtents=[0.5,0.5,0.5],
                rgbaColor=[0.85,0.15,0.15,1]
            )

            obstacle_collision = p.createCollisionShape(
                p.GEOM_BOX,
                halfExtents=[0.5,0.5,0.5]
            )

            p.createMultiBody(
                baseMass=0,
                baseCollisionShapeIndex=obstacle_collision,
                baseVisualShapeIndex=obstacle_visual,
                basePosition=[x,y,terrain_z + 0.5]
            )

# =========================================================
# START MARKER
# =========================================================

start_visual = p.createVisualShape(
    p.GEOM_CYLINDER,
    radius=0.5,
    length=0.05,
    rgbaColor=[0,1,0,1]
)

start_collision = p.createCollisionShape(
    p.GEOM_CYLINDER,
    radius=0.5,
    height=0.05
)

p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=start_collision,
    baseVisualShapeIndex=start_visual,
    basePosition=[0,0,0.15]
)

# =========================================================
# GOAL MARKER
# =========================================================

goal_x = goal[1] * 2.5
goal_y = -goal[0] * 2

goal_visual = p.createVisualShape(
    p.GEOM_CYLINDER,
    radius=0.6,
    length=0.05,
    rgbaColor=[0,0.45,1,1]
)

goal_collision = p.createCollisionShape(
    p.GEOM_CYLINDER,
    radius=0.6,
    height=0.05
)

p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=goal_collision,
    baseVisualShapeIndex=goal_visual,
    basePosition=[
        goal_x,
        goal_y,
        get_height(goal_x) + 0.25
    ]
)

# =========================================================
# HEURISTIC
# =========================================================

def heuristic(a,b):

    return math.sqrt(
        (a[0]-b[0])**2 +
        (a[1]-b[1])**2
    )

# =========================================================
# A* ALGORITHM
# =========================================================

def astar(start,goal):

    open_set = []

    heapq.heappush(open_set,(0,start))

    came_from = {}

    g_score = {start:0}

    while open_set:

        current = heapq.heappop(open_set)[1]

        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        neighbors = [

            (0,1),
            (1,0),
            (0,-1),
            (-1,0),

            (1,1),
            (1,-1),
            (-1,1),
            (-1,-1)

        ]

        for dx,dy in neighbors:

            neighbor = (
                current[0]+dx,
                current[1]+dy
            )

            r,c = neighbor

            if r < 0 or r >= ROWS or c < 0 or c >= COLS:
                continue

            if grid[r][c] == 1:
                continue

            move_cost = math.sqrt(dx*dx + dy*dy)

            tentative_g = (
                g_score[current] + move_cost
            )

            if neighbor not in g_score or tentative_g < g_score[neighbor]:

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score = (
                    tentative_g +
                    heuristic(neighbor,goal)
                )

                heapq.heappush(
                    open_set,
                    (f_score,neighbor)
                )

    return []

# =========================================================
# COMPUTE PATH
# =========================================================

path = astar(start,goal)

print("Computed Path:")
print(path)

# =========================================================
# CONVERT TO WORLD COORDS
# =========================================================

waypoints = []

for r,c in path:

    x = c * 2.5
    y = -r * 2

    waypoints.append((x,y))

# =========================================================
# DRAW PATH
# =========================================================

for i in range(len(waypoints)-1):

    p.addUserDebugLine(
        [
            waypoints[i][0],
            waypoints[i][1],
            get_height(waypoints[i][0]) + 0.15
        ],
        [
            waypoints[i+1][0],
            waypoints[i+1][1],
            get_height(waypoints[i+1][0]) + 0.15
        ],
        [1,1,0],
        lineWidth=6
    )

# =========================================================
# SMOOTH MOVEMENT
# =========================================================

current_x = 0
current_y = 0

for wp in waypoints:

    target_x,target_y = wp

    dx = target_x - current_x
    dy = target_y - current_y

    yaw = math.atan2(dy,dx)

    pitch = 0

    if target_x > 24:
        pitch = -0.18

    quat = p.getQuaternionFromEuler([0,pitch,yaw])

    # =====================================================
    # TERRAIN SPEEDS
    # =====================================================

    if target_x < 12:

        terrain = "SMOOTH TERRAIN"
        steps = 420

    elif target_x < 24:

        terrain = "ROUGH TERRAIN"
        steps = 620

    else:

        terrain = "SLOPE TERRAIN"
        steps = 900

    print("Current Terrain:", terrain)

    # =====================================================
    # MOVE ROVER
    # =====================================================

    for step in range(steps):

        t = step / steps

        x = current_x + dx * t
        y = current_y + dy * t

        z = get_height(x) + 0.18

        p.resetBasePositionAndOrientation(
            robot,
            [x,y,z],
            quat
        )

        p.stepSimulation()

        time.sleep(1/240)

    current_x = target_x
    current_y = target_y

print("GOAL REACHED!")

# =========================================================
# KEEP WINDOW OPEN
# =========================================================

while True:

    p.stepSimulation()

    time.sleep(1/240)
