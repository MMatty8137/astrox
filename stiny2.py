from PIL import Image
import numpy as np
from numpy import average 
from skyfield import api
from skyfield import almanac

# open specific cloud
im = Image.open(r'dataset\sample_crop\zchop.meta.x000.y000.n011.jpg') # Can be many different formats.
pix = im.load()

# get the width and height of the image for iterating over
print(im.size)  

# set coordinates from AI model
x = 294
y = 199
angle = 310 # set the angle (formatted as reduced edoov coefficient) for search, i.e. clockwise

# calculate meta angle
angle_radians =np.radians(angle)
x_increase_meta = np.sin(angle_radians)
y_increase_meta = np.cos(angle_radians)
y_increase_meta = -y_increase_meta
x_increase_meta = np.round(x_increase_meta,5)
y_increase_meta = np.round(y_increase_meta,5)
print(x_increase_meta, y_increase_meta)
x_increase_meta_abs = abs(x_increase_meta)
y_increase_meta_abs = abs(y_increase_meta)

# divide into quadrant and basic angle information
if 0 <= angle <= 90:
    q = 1
    angle_final = angle 
if 90 < angle <= 180:
    q = 2
    angle_final = angle - 90
if 180 < angle <= 270:
    q = 3
    angle_final = angle - 180
if 270 < angle <= 360:
    q = 4
    angle_final = angle - 270

# make at least one variable 1 and the other smaller than 1
if x_increase_meta_abs > y_increase_meta_abs:
    x_increase_final = 1
    y_increase_final = y_increase_meta_abs/x_increase_meta_abs
if x_increase_meta_abs == y_increase_meta_abs:
    x_increase_final = 1
    y_increase_final = 1
if x_increase_meta_abs < y_increase_meta_abs:
    x_increase_final = x_increase_meta_abs/y_increase_meta_abs
    y_increase_final = 1
if angle_final == 0:
    x_increase_final = 0
    y_increase_final = 1

# set absolute final values
x_increase_final_abs = abs(x_increase_final)
y_increase_final_abs = abs(y_increase_final)

# set values for future reference
## do not alter the sums or code will break
y_sum = 0
x_sum = 0
count = 0
## set how many pixel you want to count via limit
limit = 50
## do not alter list_of_values
list_of_values = []

# clear the whole txt file
with open('stiny.txt', 'w') as f:
    f.write("\n")
# put quarter information back for pixel reading
## first two lines in each if condition are mostly legacy for backwards-compatibility, code should function without them though not tested yet
if q == 1:
    x_increase_final = x_increase_final
    y_increase_final = -y_increase_final
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            x += 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            x += 1
            y -= 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            y -= 1
            x_sum += x_increase_final_abs
        #write into txt
        with open('stiny.txt', 'a') as f:
            value = str(value)
            f.write(value)
            f.write("\n")
        if count > limit:
            break
if q == 2:
    x_increase_final = x_increase_final
    y_increase_final = y_increase_final   
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            x += 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            x += 1
            y += 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            y += 1
            x_sum += x_increase_final_abs
            #write into txt
        with open('stiny.txt', 'a') as f:
            value = str(value)
            f.write(value)
            f.write("\n")
        if count > limit:
            break
if q == 3:
    x_increase_final = -x_increase_final
    y_increase_final = y_increase_final 
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            x -= 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            x -= 1
            y += 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            y += 1
            x_sum += x_increase_final_abs
        #write into txt
        value = str(value)
        with open('stiny.txt', 'a') as f:
            f.write(value)
            f.write("\n")
        if count > limit:
            break
if q == 4:
    x_increase_final = -x_increase_final
    y_increase_final = -y_increase_final 
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            x -= 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            x -= 1
            y -= 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            list_of_values.append(value)
            list_of_values.append(value)
            # add to y_sum and move pixel x for 1
            y -= 1
            x_sum += x_increase_final_abs
        #write into txt
        with open('stiny.txt', 'a') as f:
            value = str(value)
            f.write(value)
            f.write("\n")
        if count > limit:
            break

# print for debugging
print(x_increase_final, y_increase_final)

# set absolute final values
x_increase_final_abs = abs(x_increase_final)
y_increase_final_abs = abs(x_increase_final)

# find items in list correspoding to the lowest and highest point
print(list_of_values)
shadow_low = min(list_of_values)
cloud_high = max(list_of_values)

# find of said items in the list (their order)
shadow_location = list_of_values.index(shadow_low)
cloud_location = list_of_values.index(cloud_high)

# find difference between the two pixel lenghts
shadow_lenght = shadow_location - cloud_location
print(shadow_lenght)

# define a simple function to calculate distance based on a given FOV and distance in pixels
def distance(fieldOfView, distanceinpixels):
    fieldOfViewRadians = fieldOfView*(np.pi/180)
    distanceinmeters = int(distanceinpixels)*142
    return distanceinmeters

# calculate distance using said function
lenght = distance(60, shadow_lenght)
print("Shadow is exactly", lenght, "meters from the cloud!")
      
# use the NASA API to be able to calculate sun's position
ts = api.load.timescale()
ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

# define sky objects
sun = ephem["Sun"]
earth = ephem["Earth"]

# define where photo was taken(usually via EXIF data)
coordinates_latitude = "49.73880 N"
coordinates_longtitude = "13.39350 E"
# given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
sun_pos = (earth + location).at(ts.now()).observe(sun).apparent()
altitude, azimuth, distance = sun_pos.altaz()

print(f"Azimuth: {azimuth.degrees:.4f}")
print(f"Altitude: {altitude.degrees:.4f}")

# calculate final values
altitude= int(altitude.degrees)
cloudheight = np.tan(altitude)*lenght

print("Shadow is exactly", cloudheight, "meters from ground!")

