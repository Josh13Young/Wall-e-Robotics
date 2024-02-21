from bot_control.TestBot import TestBot

def main():
    bot = TestBot()
    
    while True:
        measurement = bot.get_ultrasonic_sensor_value()
        print(f"Distance: {measurement}cm")

if __name__ == "__main__":
    main()

'''
Distances measured from the front of the top of sonar.

1. When placed facing and perpendicular to a smooth surface such as a wall, what are the minimum
and maximum depths that the sensor can reliably measure?
    - Minimum reliable measurement: ~10cm
    - Maximum reliable measurement: ~220cm

2. Move the sonar so that it faces the wall at a non-orthogonal incidence angle. What is the maximum angular deviation from perpendicular to the wall at which it will still give sensible readings?
    - At a distance of ~80cm an angle of ~25deg is the maximum angle that gives sensible readings. 

3. Do your sonar depth measurements have any systematic (non-zero mean) errors? To test this, set
up the sensor at a range of hand-measured depths (20cm, 40cm, 60cm, 80cm, 100cm) from a wall
and record depth readings. Are they consistently above or below what they should be?
    - True: 20cm  Sonar: 21cm
    - True: 40cm  Sonar: 40cm
    - True: 60cm  Sonar: 60cm
    - True: 80cm  Sonar: 80cm
    - True: 100cm Sonar: 100cm

4. What is the the accuracy of the sonar sensor and does it depend on depth? At each of two chosen
hand-measured depths (40cm and 100cm), make 10 separate depth measurements (each time
picking up and replacing the sensor) and record the values. Do you observe the same level of
scatter in each case?
    - 40cm:  40, 39, 40, 40, 40, 39, 40, 40, 40, 39
    - 100cm: 100, 100, 99, 100, 100, 99, 100, 99, 100, 100

5. In a range of general conditions for robot navigation, what fraction of the time do you think your
sonar gives garbage readings very far from ground truth?
    - If an object in front of the sonar is not flat and smooth, reported distances will be very irregular and unstable. Also, during motion the robot may not be moving on smooth ground causing detection of sound reflection to be distorted. Also, from far distances, interference may cause the robot to produce innacurate readings. Overall we should expect that up to ~5% of the readings at any given time will be very far from the ground truth.
    
'''

