
import math
import random
import time
from particleDataStructures import canvas, mymap
import brickpi3
BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_C # right motor
motorL = BP.PORT_B # left motor
from bot_control.PositionControl import Bot
bot = Bot()
bot.set_motor_limits(35)

##  Holds the particles and weights (NO MORE GLOBAL 😁)
class Positions:
    def __init__(self):
        self.particles = [(float(84), float(30), float(0)) for _ in range(100)]
        self.weights = [1 / len(self.particles) for _ in range(len(self.particles))]

    # Draws all particles
    def draw(self):
        canvas.drawParticles(self.particles)

    # Calculates new nx, ny, ntheta of the robot
    def get_new_avg_pos(self):
        x_bar = sum([self.weights[i] * self.particles[i][0] for i in range(len(self.particles))])
        y_bar = sum([self.weights[i] * self.particles[i][1] for i in range(len(self.particles))])
        theta_bar = sum([self.weights[i] * self.particles[i][2] for i in range(len(self.particles))])
        return x_bar, y_bar, theta_bar

    def normalise(self):
        new_weights = []
        total = sum(self.weights)
        for weight in self.weights:
            new_weights.append(weight / total)
        self.weights = new_weights

    def resample(self):   # Follows spec method
        n = len(self.particles)
        new_particles = []
        # Build cumulative weights array
        cumulative_weights = [sum(self.weights[:i+1]) for i in range(n)]
        # Generate new particles
        for _ in range(n):
            random_number = random.random()
            # Find the index in the cumulative weights array where the random number falls
            for i in range(n):
                if random_number <= cumulative_weights[i]:
                    new_particles.append(self.particles[i])
                    break
                
        self.particles = new_particles
        # Resets weights to all be equal because after resampling each particle should have an equal chance of being selected
        self.weights = [1 / len(self.particles) for _ in range(len(self.particles))] 


    # TODO: Our original method, we should test both this and the spec version
    # def resample(self):
    #     population = random.choices(list(zip(self.particles, self.weights)), weights=self.weights, k=100)
    #     [self.particles, weights] = list(zip(*population))
    #     self.weights = [1 / len(self.particles) for _ in range(len(self.particles))]

positions = Positions()


##  All the walls of the arena
walls = {
    1: ((210, 84), (210, 0)),
    2: ((168, 84), (210, 84)),
    3: ((0, 0), (0, 168)),
    4: ((84, 210), (168, 210)),
    5: ((84, 126), (84, 210)),
    6: ((210, 0), (0, 0)),
    7: ((0, 0), (0, 168)),
    8: ((210, 0), (0, 0))
}


################## CODE #####################

def calc_angle(theta, wall):
    (a_x, a_y), (b_x, b_y) = wall
    num = (math.cos(theta))*(a_y - b_y) + (math.sin(theta))*(b_x - a_x)
    den = math.sqrt((a_y - b_y)**2 + (b_x - a_x)**2)

    return (math.acos(num/den))

# Forward distance between the robot and a wall
def wall_dist(x, y, theta, wall):
    (a_x, a_y), (b_x, b_y) = wall
    q = (b_y - a_y)*(math.cos(theta)) 
    r = (b_x - a_x)*(math.sin(theta))
    if (q - r) == 0:
        return float('inf')
    m = ((b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)) / (q-r)
    x_satisfied = (a_x <= x + m * math.cos(theta) <= b_x or b_x <= x + m * math.cos(theta) <= a_x)
    y_satisfied = (a_y <= y + m * math.sin(theta) <= b_y or b_y <= y + m * math.sin(theta) <= a_y)
    print("x" + str(x_satisfied) + " y" + str(y_satisfied))
    if x_satisfied and y_satisfied:
        return m
    return float('inf')

# Returns the distance to the closest wall and the wall which robot should be facing
def find_dist_to_closest_wall(x, y, theta) -> tuple[float, tuple[float, float]] :
    min_m = float('inf')
    min_wall = None
    for wall in walls.values():
        
        m = wall_dist(x, y, theta, wall)
        if m < 0:
            continue
        if m < min_m:
            min_m = m
            min_wall = wall

    if min_wall is None:
        raise ValueError("Robot is not facing any wall. Enclosed arena assumption violated.")
      
    return min_m, min_wall


# find likelihood
def calculate_likelihood(x, y, theta, z):
    # TODO: Experiment with sigma and K
    sigma = 0.02
    K = 0.5
    m, _ = find_dist_to_closest_wall(x, y, theta)
    return math.exp((-(-z-m)**2)/2*sigma**2) + K


# Handles the mcl steps
def mcl_update(was_turn, x, y, theta, distance, angle):
    sonars = [bot.get_ultrasonic_sensor_value() for _ in range(10)]
    sonar = sum(sonars) / len(sonars)   # Avg sonar readings
    # Skip all weight/mcl updates if angle to closest wall is > 15
    _, wall = find_dist_to_closest_wall(x, y, theta)
    skip_update = calc_angle(theta, wall) > 15

    new_particles = []
    if not was_turn:   # Do random gauss + likelihood for forward motion
        for i in range(len(positions.particles)):
            e = random.gauss(0, 0.02)
            f = random.gauss(0, 0.015)
            theta = positions.particles[i][2]
            lst = list(positions.particles[i])
            lst[0] += (distance + e) * math.cos(theta)
            lst[1] += (distance + e) * math.sin(theta)
            lst[2] += f
            particle = tuple(lst)
            new_particles.append(particle)

            if not skip_update:
                likelihood = calculate_likelihood(lst[0], lst[1], lst[2], sonar)
                positions.weights[i] = likelihood * positions.weights[i]            

    else:   # Do random gauss + likelihood for turning motion
        for i in range(len(positions.particles)):
            theta = positions.particles[i][2]
            g = random.gauss(0, 0.01)
            lst = list(positions.particles[i])
            lst[2] += angle + g
            particle = tuple(lst)
            new_particles.append(particle)

            if not skip_update:
                likelihood = calculate_likelihood(lst[0], lst[1], lst[2], sonar)
                positions.weights[i] = likelihood * positions.weights[i]
    
    positions.particles = new_particles

    if not skip_update:
        positions.normalise()
        positions.resample()
    
    positions.draw()
    return positions.get_new_avg_pos()


# Moves robot 20cm/remainder of drive amount, does the 4 mcl update steps and thats it
def move_robot(x, y, theta, wx, wy):
    centimeter = 833 / 40
    rotate = 1080
    x_new, y_new = wx - x, wy - y
    angle = math.degrees(math.atan2(y_new, x_new)) - theta
    dist = math.sqrt(x_new**2 + y_new**2)
    motorDriveAmount = centimeter * dist    # How much the wheels turn to reach the waypoint forward

    print("angle: " + str(angle))
    if angle < -180:
        angle += 360
    elif angle > 180:
        angle -= 360
    motorTurnAmount = rotate * (angle / 360)    # How much the wheels turn to reach the waypoint turning

    
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
    BP.set_motor_position(motorR, pos_r + motorTurnAmount)
    BP.set_motor_position(motorL, pos_l - motorTurnAmount)
    mcl_update(True, x, y, theta, 0, math.radians(angle))     # TODO: should the overall position change every turn? idts bc then it wont decide whether to move or turn again
    time.sleep(1.5)
    
    # Move 20 else the remainder
    if motorDriveAmount > centimeter * 20:
        motionAmount = centimeter * 20
        dist = 20
    else:
        motionAmount = motorDriveAmount
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
    BP.set_motor_position(motorR, pos_r + motionAmount)
    BP.set_motor_position(motorL, pos_l + motionAmount)
    time.sleep(1)
    nx, ny, ntheta = mcl_update(False, x, y, theta, dist, 0)
    print(nx, ny, ntheta)
    return nx, ny, ntheta + angle   # TODO: I think this is the correct way to update the overall position of the robot for the next iteration

# Continuously moves robot towards given waypoint until within threshhold distance
def navigateToWaypoint(x, y, theta, wx, wy):
    threshhold = 1  # Used to decide whether to keep moving towards waypoint
    nx, ny, ntheta = move_robot(x, y, theta, wx, wy)
    while (abs(nx - wx) > threshhold and abs(ny - wy) > threshhold):
        x, y, theta = nx, ny, ntheta
        nx, ny, ntheta = move_robot(x, y, theta, wx, wy)
    return nx, ny, ntheta

# Moves robot to all waypoints
def navigateToAllWaypoints(x, y, theta):
    waypoints = [(180, 30), (180, 54), (138, 54), (138, 168), (114, 168), (114, 84), (84, 84), (84, 30)]
    nx, ny, ntheta = x, y, theta
    for wx, wy in waypoints:
        nx, ny, ntheta = navigateToWaypoint(nx, ny, ntheta, wx, wy)
        time.sleep(1)

# MAIN:
try:
    mymap.draw()
    waypoint1 = (84, 30, 0)
    navigateToAllWaypoints(waypoint1[0], waypoint1[1], waypoint1[2])
    

except KeyboardInterrupt:
    BP.reset_all()