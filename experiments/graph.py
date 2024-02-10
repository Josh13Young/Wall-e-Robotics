
particles = [(1, 1, 90), (300, 200, 0), (500, 700, 180)]
def square_graph():
    line1 = (0, 0, 0, 500)
    line2 = (500, 500, 500, 0)
    line3 = (0, 500, 500, 500)
    line4 = (0, 0, 500, 0)
    print("drawLine:" + str(line1))
    print("drawLine:" + str(line2)) 
    print("drawLine:" + str(line3)) 
    print("drawLine:" + str(line4)) 



print ("drawParticles:" + str(particles))
square_graph()