import time
import math

import csv
import re

# global variable 
value = 1

controlDown = False
shiftDown = False

degree_symbol = u"\N{DEGREE SIGN}"

total_distance = 0

starting_point = [0,0]

count = 0
manual_simulated_points = []
robot_running_points = []

yaw_and_rel_pos = []

distances = []
degrees = []

cf = 2/3 # Conversion Factor
delta = 0.0000000001 # Small constant used to replace undefined slope

#def scaleRatioX(x):
    


# function to setup size of
# output window
def setup():
    background(255)
    x = 2362
    y = 1143
    
    while x >= displayWidth:
        x -= 1
        
    while y >= displayHeight:
        y -= 1
        
    while x/y != 2362/1143:
        y -= 1

    image(loadImage("submerged.jpg"), 0, 100, x, y)
    
    fill(0)
    
    text("(0, 0)\n1", starting_point[0] + 15, starting_point[1])
    
    size(displayWidth, displayHeight)
    #fullScreen()
    # Toolbar
    image(loadImage("download_button.jpg"), 0, 0, 100, 100) # Download Button
    #image(loadImage("connect.jpg"), 100, 1143 * 2/3, 100, 100) # Connect Button
    image(loadImage("calculate.jpg"), 200, 0, 100, 100) # Calculate Button
    image(loadImage("robot_data_gen.jpg"), 300, 0, 100, 100) # Robot Simulate Points Button
    
# def fileSelected(selection):
#     print("selection")
#     if selection == None:
#         print("Window was closed or the user hit cancel.")
#     else:
#         print("selected")
#         image(loadImage(selection.getAbsolutePath(), 0, 0, 2362 * 2/3, 1143 * 2/3))

# function to enable drawing on the window
def draw(): 
    pass

def rel_pos_to_pxl(rel_pos):
    mm = rel_pos * 55/72
    pxl = mm * displayWidth / 2362
    
    return pxl

def pxl_to_rel_pos(pxl):
    mm = pxl * 2362 / displayWidth
    rel_pos = mm * 72/55
    
    return rel_pos

def connect_lines(color_value, points):
    global total_distance
    
    output = []
    
    stroke(color_value)
    fill(color_value)
    
    for first, second in zip(points[:-1], points[1:]): # Make line between points
        distance = sqrt((second[0] - first[0])**2 + (second[1] - first[1])**2)
        distance = round(distance, 2)
        
        total_distance += distance
        
        output.append([first, second, distance])
        
        line(first[0], first[1], second[0], second[1])
        
        label_x = (first[0] + second[0])/2
        label_y = (first[1] + second[1])/2
        
        text(str(round(pxl_to_rel_pos(distance * 3/2), 2)) + " RP", label_x - 5, label_y - 5)
        
    stroke(0)
    fill(0)
    
    return output

def calculate_angle(m1, m2):
    #([///ANGLES///])
    angle_radians = math.atan(abs((m2 - m1) / (1 + m1 * m2)))
    angle_degrees = angle_radians * 180 / math.pi
    
    return angle_degrees
    
def mousePressed():
    global total_distance
    global robot_running_points
    global manual_simulated_points
    global distances
    global count
    global value
    global starting_point
    
    if len(manual_simulated_points) == 0:
            starting_point = [mouseX, mouseY]
            # width of circle
            r = 10
            
            fill(0)
            
            count = 0
            total_distance = 0
            
            ellipse(starting_point[0], starting_point[1], 10, 10)
        
            text("(0, 0)\n1", starting_point[0] + 15, starting_point[1])
        
            # to create a circle at the position of mouseX, mouseY
            ellipse(mouseX, mouseY, r, r)
            
            count += 1
            
            manual_simulated_points.append([mouseX, mouseY])
            
    elif mouseY > 100: # Draw point
        # width of circle
        r = 10
        
        fill(0)
        
        count = 0
        total_distance = 0
        
        ellipse(starting_point[0], starting_point[1], 10, 10)
    
        text("(0, 0)\n1", starting_point[0] + 15, starting_point[1])
    
        # to create a circle at the position of mouseX, mouseY
        ellipse(mouseX, mouseY, r, r)
        
        count += 1
        
        manual_simulated_points.append([mouseX, mouseY])
        print([mouseX, mouseY])
        
        total_distance = 0
        
        connect_lines(color(0), manual_simulated_points)
        
        global delta
        global degree_symbol
        
        m1 = (manual_simulated_points[1][1] - starting_point[1])/delta
        delta_x = manual_simulated_points[-2][0] - manual_simulated_points[-1][0] #x2 - x1
        if delta_x != 0:
            delta_y = manual_simulated_points[-2][1] - manual_simulated_points[-1][1]
            m2 = float(delta_y)/float(delta_x) #(y2 - y1)/(x2 - x1)
        else:
            m2 = (manual_simulated_points[-1][1] - manual_simulated_points[-2][1])/delta
        
        txt = "(" + str(round(pxl_to_rel_pos(total_distance * 3/2), 2)) + ", " + str(round(calculate_angle(m1, m2))) + degree_symbol + ")\n1"
        
        text(txt, mouseX + 15, mouseY)
        
    elif mouseX < 100: # Download Button Click
        global manual_simulated_points
        
        # open file
        with open('C:/Users/6052h/Downloads/manual_simulated_points.txt', 'w+') as f:
            
            # write elements of list
            for item in manual_simulated_points:
                f.write('%s\n' %item)
            
            print("File written successfully")
        
        # close the file
        f.close()
        
        with open('C:/Users/6052h/Downloads/distances.txt', 'w+') as f:
            
            # write elements of list
            for item in distances:
                f.write('%s\n' %item)
        
            print("File written successfully")
        
        # close the file
        f.close()
        
        with open('C:/Users/6052h/Downloads/degrees.txt', 'w+') as f:
            
            # write elements of list
            for item in degrees:
                f.write('%s\n' %item)
            

            print("File written successfully")
        
        # close the file
        f.close()
        
        with open('C:/Users/6052h/Downloads/robot_running_points.txt', 'w+') as f:
            
            # write elements of list
            for item in robot_running_points:
                f.write('%s\n' %item)
            

            print("File written successfully")
        
        # close the file
        f.close()
            
    elif 200 < mouseX < 300:
        global total_distance
            
        fill(255)
        square(300, 0, 100)
        fill(0)
        
        text(str(round(total_distance * 3/2 * (1 + 7 / 23), 2)) + " RP,\n" + str(round(total_distance * 1/50, 2)) + " seconds", 305, mouseY)
        
    elif 300 < mouseX < 400:
        pattern = re.compile(r"([0-9]*);([0-9]*\.?[0-9]*);([0-9]*\.?[0-9]*)", re.IGNORECASE)
        List = []

        with open("collect-perfect.csv") as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                result = pattern.match(row[0])
        
                if result:
                    List.append([result.group(1), result.group(2), result.group(3)])
        #print(List)
        global manual_simulated_points
        
        last_point = manual_simulated_points[0]
        robot_running_points.append(last_point)
        last_yaw = 0
        
        fill(255,0,0)
        for i in range(len(List)):
            print("for loop")
            if List[i][2] == '': # If straight line
                print("straight")
                
                angle = math.radians(float(last_yaw))
                print("angle: ", angle)
                
                a = float(List[i][1]) * math.sin(angle)
                b = float(List[i][1]) * math.cos(angle)
                
                print(a,b)
                print(rel_pos_to_pxl(a), rel_pos_to_pxl(b))
                new_x = last_point[0] + rel_pos_to_pxl(a)
                #print("new_x")
                new_y = last_point[1] - rel_pos_to_pxl(b)
                #print("new_y")
                
                print([new_x, new_y])
                ellipse(new_x, new_y, 10, 10)
                
                last_point = [new_x, new_y]
                
                robot_running_points.append(last_point)
            else: # If turn
                print("turn")
                last_yaw = List[i][2]
                
        connect_lines(color(255,0,0), robot_running_points)
        fill(0)
        
def undo():
    if manual_simulated_points:
        global count
        global distances
        global robot_running_points
        global starting_point
        global delta
        global degree_symbol
        
        manual_simulated_points.pop()
        
        distances = []
        degrees = []
        robot_running_points = []
        
        image(loadImage("submerged.jpg"), 0, 0, 2362 * 2/3, 1143 * 2/3)
        print("loadimage")
        count = 0
        print(manual_simulated_points)
        for group in manual_simulated_points:
            ellipse(starting_point[0], starting_point[1], 10, 10)
            
            text("(0, 0)\n1", starting_point[0] + 15, starting_point[1])
            # to create a circle at the position of mouseX, mouseY
            ellipse(group[0], group[1], 10, 10)
            
            count += 1
            
            total_distance = 0
            
            connect_lines(color(0), manual_simulated_points)
            
            m1 = (manual_simulated_points[1][1] - starting_point[1])/delta
            delta_x = manual_simulated_points[-2][0] - manual_simulated_points[-1][0] #x2 - x1
            if delta_x != 0:
                delta_y = manual_simulated_points[-2][1] - manual_simulated_points[-1][1]
                m2 = float(delta_y)/float(delta_x) #(y2 - y1)/(x2 - x1)
            else:
                m2 = (manual_simulated_points[-1][1] - manual_simulated_points[-2][1])/delta
            
            txt = "(" + str(round(pxl_to_rel_pos(total_distance * 3/2), 2)) + ", " + str(round(calculate_angle(m1, m2))) + degree_symbol + ")\n1"
            
            text(txt, group[0] + 15, group[1])

def keyPressed():
    if key == "z":
        undo()
