from exif import Image
from datetime import datetime
import cv2
import math
import numpy as np
from orbit import ISS

#def get_time(image):
#    with open(image, 'rb') as image_file:
#        img = Image(image_file)
#        time_str = img.get("datetime_original")
#        time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
#    return time
#def get_time_difference(image_1, image_2):
#    time_1 = get_time(image_1)
#    time_2 = get_time(image_2)
#    time_difference = time_2 - time_1
#    print("time_difference", time_difference)
#    return time_difference.seconds
def get_time_difference(image_1, image_2):
    return "1q"

def convert_to_cv(image_1, image_2):
    image_1_cv = cv2.imread(image_1, 0)
    image_2_cv = cv2.imread(image_2, 0)
    return image_1_cv, image_2_cv

def calculate_features(image_1, image_2, feature_number):
    orb = cv2.ORB_create(nfeatures = feature_number)
    keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
    keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
    return keypoints_1, keypoints_2, descriptors_1, descriptors_2

def calculate_matches(descriptors_1, descriptors_2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = brute_force.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    return matches

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    global x_1all_div
    global x_2all_div
    global y_1all_div
    global y_2all_div
    x_1all=0
    x_2all=0
    y_1all=0
    y_2all=0
    counter=0
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
        counter+=1    
        x_1all=x_1all+x1
        x_2all=x_2all+x2
        y_1all=y_1all+y1
        y_2all=y_2all+y2
    x_1all_div=x_1all/counter
    x_2all_div=x_2all/counter
    y_1all_div=y_1all/counter
    y_2all_div=y_2all/counter
    print(x_1all_div)
    print(x_2all_div)
    print(y_1all_div)
    print(y_2all_div)

    global direction_x
    global direction_y
    delta_x = x_1all_div-x_2all_div
    if delta_x > 0:
        direction_x = "left"
    elif delta_x < 0:
        direction_x = "right"
    else: 
        direction_x = "null"
    delta_y = y_1all_div-y_2all_div
    if delta_y > 0:
        direction_y = "up"
    elif delta_y < 0:
        direction_y = "down"
    else:
        direction_y = "null"

    delta_x = abs(delta_x)
    delta_y = abs(delta_y)

    tangens_angle_for_general_direction_radians = np.arctan((delta_y)/(delta_x))
    tangens_angle_for_general_direction_degrees = tangens_angle_for_general_direction_radians * (360/(2*np.pi))
    print("Tan angle for direction:", tangens_angle_for_general_direction_degrees, "therefore IMAGE shifted", direction_x, direction_y)


    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)
import statistics

def calculate_median_tgangle(coordinates_1, coordinates_2):
    all_tgangles = []
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        if x_difference != 0:
            tgangle = y_difference / (x_difference)
            all_tgangles.append(tgangle)
    return statistics.median(all_tgangles)

def calculate_mean_tgangle(coordinates_1, coordinates_2):
    all_tgangles = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        if x_difference !=0:
            tgangle = y_difference / (x_difference)
            all_tgangles = all_tgangles + tgangle
    return all_tgangles / len(merged_coordinates)


#def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
#    distance = feature_distance * GSD / 100000
#    speed = distance / time_difference
#    return speed

latitude_before = 0 #latitude před procesem

image_1 = r'C:\Users\kiv\Downloads\eda\eda\eda315-1.jpg'
image_2 = r'C:\Users\kiv\Downloads\eda\eda\eda315-2.jpg'


time_difference = get_time_difference(image_1, image_2) 
image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
matches = calculate_matches(descriptors_1, descriptors_2)
display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
#speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
#print(speed)
#print(average_feature_distance)
average_tangens_angle = calculate_mean_tgangle(coordinates_1, coordinates_2)
print("average_tangens_angle_radians", average_tangens_angle)
median_tangens_angle = calculate_median_tgangle(coordinates_1, coordinates_2)
print("median_tangens_angle_radians", median_tangens_angle)

degrees_med = np.arctan(median_tangens_angle)*(360/(2*np.pi))
degrees_avg = np.arctan(average_tangens_angle)*(360/(2*np.pi))

print("mean_tangens_angle_degrees", degrees_med)
print("average_tangens_angle_degrees", degrees_avg)

absolute_value_degrees_med = abs(degrees_med)

edoov_coefficient = ""
if direction_x == "left":
    if direction_y == "up":
        edoov_coefficient = (absolute_value_degrees_med, -1, -1)
        reduced_edoov_coefficient = 270-absolute_value_degrees_med
    if direction_y == "down":
        edoov_coefficient = (absolute_value_degrees_med, -1, 1)
        reduced_edoov_coefficient = 270+absolute_value_degrees_med
if direction_x == "right":
    if direction_y == "up":
        edoov_coefficient = (absolute_value_degrees_med, 1, -1)
        reduced_edoov_coefficient = 90+absolute_value_degrees_med
    if direction_y == "down":
        edoov_coefficient = (absolute_value_degrees_med, 1, 1)
        reduced_edoov_coefficient = 90-absolute_value_degrees_med

negated_reduced_edoov_coefficient = reduced_edoov_coefficient+180
if negated_reduced_edoov_coefficient > 360:
    negated_reduced_edoov_coefficient-=360
print(edoov_coefficient)
print("obraz", reduced_edoov_coefficient)
print("let", negated_reduced_edoov_coefficient)

latitude_after = 0 #latitude po procesu

alpha_k=np.arcsin((np.cos(51.6*(np.pi/180)))/(np.cos(latitude*(np.pi/180))))
alpha_k = alpha_k*(180/np.pi)

corrected_alpha_k=0

print("alfonsoov koeficient", alpha_k)
poloha_severu=360-reduced_edoov_coefficient-alpha_k
print("Poloha severu: ",poloha_severu)

print(f'Latitude: {location.latitude}')
print(f'Longitude: {location.longitude}')
print(f'Elevation: {location.elevation.km}')



