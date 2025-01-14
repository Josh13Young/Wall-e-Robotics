
import math
import random
import time
from bot_control.PositionControl import PositionControlBot, Bot
from particleDataStructures import canvas, mymap
import brickpi3

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_C # right motor
motorL = BP.PORT_B # left motor

from typing import Tuple, Dict

Coordinate = Tuple[int, int]
Wall = Tuple[Coordinate, Coordinate]

walls: Dict[int, Wall] = {
    1: ((210, 84), (210, 0)),
    2: ((168, 84), (210, 84)),
    3: ((0, 0), (0, 168)),
    4: ((84, 210), (168, 210)),
    5: ((84, 126), (84, 210)),
    6: ((210, 0), (0, 0)),
    7: ((0, 0), (0, 168)),
    8: ((210, 0), (0, 0))
}

wall = None
particles = [(float(84), float(30), float(0)) for _ in range(100)]
weights = [1 / len(particles) for _ in range(len(particles))]
forward_dist=833
turn_amount=256

def wall_dist(x, y, theta, wall: Wall):
    (a_x, a_y), (b_x, b_y) = wall
    return ((b_y - a_y)*(a_x - x) - (b_x - a_x)*(a_y - y)) / ((b_y - a_y)*math.degrees(math.cos(theta)) - (b_x - a_x)*math.degrees(math.sin(theta)))


def find_closest_wall(x, y, theta):
    # global current_wall
    # return walls[current_wall]
    # will change to code below
    min_m = float('inf')
    min_wall = None
    for wall in walls.values():
        m = wall_dist(x, y, theta, wall)
        if m < min_m:
            min_m = m
            min_wall = wall
            
    if min_m < 0:
        return None
    return min_wall



def calc_angle(theta, wall: Wall):
    (a_x, a_y), (b_x, b_y) = wall
    num = math.degrees(math.cos(theta))*(a_y - b_y) + math.degrees(math.sin(theta))*(b_x - a_x)
    den = math.sqrt((a_y - b_y)**2 + (b_x - a_x)**2)
    return math.degrees(math.acos(num/den))
    


def calculate_likelihood(x, y, theta, z):
    sigma = 0.02    
    global wall
    wall = find_closest_wall(x, y, theta)

    # didn't detect a valid wall, so likelihood here is 0
    if not wall:
        return 0
    
    m = wall_dist(x, y, theta, wall)
    return math.exp((-(-z-m)**2)/2*sigma**2) + 0


def norm():
    global weights
    total = sum(weights)
    for weight in weights:
        weight = weight / total

def resample():
    global weights
    global particles
    population = random.choices(list(zip(particles, weights)), weights=weights, k=100)
    [particles, weights] = list(zip(*population))


def update_weights(sonar):
    global particles
    dist = 20
    global wall
    new_particles = []
    for i in range(len(particles)):
        e = random.gauss(0, 0.02)
        f = random.gauss(0, 0.015)

        theta = particles[i][2]

        lst = list(particles[i])
        lst[0] += (dist + e) * math.cos(theta)
        lst[1] += (dist + e) * math.sin(theta)
        lst[2] += f
        particle = tuple(lst)
        new_particles.append(particle)
        
        likelihood = calculate_likelihood(lst[0], lst[1], lst[2], sonar)
        if not wall:
            continue
        if calc_angle(theta, wall) > 15:
            print(calc_angle(theta, wall))
            continue
        weights[i] = likelihood * weights[i]
    particles = new_particles
    norm()
    resample()
    print("drawParticles:" + str(particles))

def update_weights_rotate(sonar):
    global particles
    dist = 20
    global wall
    new_particles = []
    for i in range(len(particles)):
        theta = particles[i][2]
        g = random.gauss(0, 0.01)
        lst = list(particles[i])
        lst[2] += -math.pi/2 + g
        particle = tuple(lst)
        new_particles.append(particle)
        likelihood = calculate_likelihood(lst[0], lst[1], lst[2], sonar)
        if not wall:
            continue
        if calc_angle(theta, wall) > 15:
            print(calc_angle(theta, wall))
            continue
        weights[i] = likelihood * weights[i]
    particles = new_particles
    norm()
    resample()
    print("drawParticles:" + str(particles))

def navigateToWaypoint(x, y, theta, wx, wy):
    centimeter = (833 / 40)
    rotate = 1080
    x_new, y_new = wx - x, wy - y
    angle = math.degrees(math.atan2(y_new, x_new)) - theta
    dist = math.sqrt(x_new**2 + y_new**2)
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)

    motorDriveAmount = centimeter * dist
    print("angle: " + str(angle))
    if angle < -180:
        angle += 360
    elif angle > 180:
        angle -= 360
    motorTurnAmount = rotate * (angle / 360)
    BP.set_motor_position(motorR, pos_r + motorTurnAmount)
    BP.set_motor_position(motorL, pos_l - motorTurnAmount)
    time.sleep(1)

    total_move = motorDriveAmount
    """
    Extract the division of 20 centimeter steps outside of this function, so that it moves 20cms
    then calculates the average x, y and theta of the particles and uses this as it's next position to start from
    
    """
    while total_move > centimeter * 20:
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        BP.set_motor_position(motorR, pos_r + centimeter * 20)
        BP.set_motor_position(motorL, pos_l + centimeter * 20)
        thing()
        total_move -= centimeter * 20
        print("total move", total_move)
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
    BP.set_motor_position(motorR, pos_r + total_move)
    BP.set_motor_position(motorL, pos_l + total_move)
    thing()
    nx, ny, ntheta = get_avgs()
    time.sleep(1)
    #return wx, wy, theta + angle
    return nx, ny, ntheta

# TODO: change name of 
def thing():
    time.sleep(1)
    sonars = [bot.get_ultrasonic_sensor_value() for _ in range(10)]
    print(sonars)
    sonar = sum(sonars) / len(sonars)
    update_weights(sonar)
    print(weights)
    print(particles)
    canvas.drawParticles(particles)
    time.sleep(1)

def get_avgs():
    global particles
    global weights
    x_bar = sum([weights[i] * particles[i][0] for i in range(len(particles))])
    y_bar = sum([weights[i] * particles[i][1] for i in range(len(particles))])
    theta_bar = sum([weights[i] * particles[i][2] for i in range(len(particles))])
    return x_bar, y_bar, theta_bar

try:
    bot = Bot()
    posControlBot = PositionControlBot(bot, 200)
    mymap.draw()
    print(bot.get_ultrasonic_sensor_value())
    #while True:    
    x, y, theta = navigateToWaypoint(84, 30, 0, 104, 30)
    print("x y theta ", x, y, theta)
    x, y, theta = navigateToWaypoint(x, y, theta, 124, 30)
    print("x y theta ", x, y, theta)
    x, y, theta = navigateToWaypoint(x, y, theta, 144, 30)


except KeyboardInterrupt:
    BP.reset_all()
