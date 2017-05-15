import os, csv
from pprint import pprint
data_air = []
data_glass = []

files = list(os.walk("data"))
file_count = 0
print(files)
for dataset in files[0][2]:
    with open(os.path.join("data", dataset), "r") as csv_file:
        data_air.append([[], [], [], [], [], [], [], [], [], [], []])
        data_glass.append([[], [], [], [], [], [], [], [], [], [], []])
        frequency = []
        vm = []
        vlc = []
        count = 0
        spamreader = csv.reader(csv_file, delimiter=',')
        for line in spamreader:
            count += 1
            if count != 1 and line != []:
                data_air[0][0].append(line[0])
                data_air[0][1].append(line[1])
                data_air[0][2].append(line[2])
                data_air[0][3].append(line[3])
                data_air[0][4].append(line[4])
                data_air[0][5].append(line[5])
                data_air[0][6].append(line[6])
                data_air[0][7].append(line[7])
                data_air[0][10].append(line[10])
            elif line != []:
                data_glass[0][0].append(line[0])
                data_glass[0][1].append(line[1])
                data_glass[0][2].append(line[2])
                data_glass[0][3].append(line[3])
                data_glass[0][4].append(line[4])
                data_glass[0][5].append(line[5])
                data_glass[0][6].append(line[6])
                data_glass[0][7].append(line[7])
                data_glass[0][10].append(line[10])
                data_glass[0][2] = data_air[0][2]
                data_glass[0][5] = data_air[0][5]

# Have the data, now clean it up! 0 is Glass-Air, 1 is Air-Glass
# Everything above 50 is mV, below is V when reading in data
# [0,1,2,3,4,5] are voltage measurements, [2,5] are background
# [6 is glass theta, [7 is theta 2, for transmission theta, and [10 is theta 3, reflection

# Subtract background for all values that are not '' since '' will be 0 value
def subtract_background(data_set):
    t_background = 0.0
    r_background = 0.0
    r_p = []
    r_s = []
    t_p = []
    t_s = []

    # Get average background for the two datatypes to subtract
    count = 0
    for element in data_set[0][2]:
        # T_b
        if element != '':
            count += 1
            t_background += float(element)
    t_background /= count

    count = 0
    for element in data_set[0][5]:
        # R_b
        if element != '':
            count += 1
            r_background += float(element)
    r_background /= count

    # Data points daved will be in tuple (data, theta 1, [thea 2 if T, theta 3 if R])
    for index, t_p_val in enumerate(data_set[0][0]):
        #print(t_p_val)
        if t_p_val != '':
            current_point = float(t_p_val)
            # Take care of V vs mV, change V to mV
            if current_point <= 10.0:
                current_point *= 1000
        else:
            current_point = 0.0

        if current_point != 0.0:
            # subtract the background
            # Tb is [2]
            if current_point >= t_background:
                current_point -= t_background
            else:
                current_point = 0.0

        t_p.append((current_point, float(data_set[0][6][index]), float(data_set[0][7][index])))

    # Data points daved will be in tuple (data, theta 1, [thea 2 if T, theta 3 if R])
    for index, t_s_val in enumerate(data_set[0][1]):
        #print(t_p_val)
        if t_s_val != '':
            current_point = float(t_s_val)
            # Take care of V vs mV, change V to mV
            if current_point <= 10.0:
                current_point *= 1000
        else:
            current_point = 0.0

        if current_point != 0.0:
            # subtract the background
            # Tb is [2]
            if current_point >= t_background:
                current_point -= t_background
            else:
                current_point = 0.0

        t_s.append((current_point, float(data_set[0][6][index]), float(data_set[0][7][index])))

    # Data points daved will be in tuple (data, theta 1, [thea 2 if T, theta 3 if R])
    for index, r_p_val in enumerate(data_set[0][3]):
        #print(t_p_val)
        if r_p_val != '':
            current_point = float(r_p_val)
            # Take care of V vs mV, change V to mV
            if current_point <= 10.0:
                current_point *= 1000
        else:
            current_point = 0.0

        if current_point != 0.0:
            # subtract the background
            # Tb is [2]
            if current_point >= r_background:
                current_point -= r_background
            else:
                current_point = 0.0

        r_p.append((current_point, float(data_set[0][6][index]), float(data_set[0][10][index])))

    # Data points daved will be in tuple (data, theta 1, [thea 2 if T, theta 3 if R])
    for index, r_s_val in enumerate(data_set[0][0]):
        #print(t_p_val)
        if r_s_val != '':
            current_point = float(r_s_val)
            # Take care of V vs mV, change V to mV
            if current_point <= 10.0:
                current_point *= 1000
        else:
            current_point = 0.0

        if current_point != 0.0:
            # subtract the background
            # Tb is [2]
            if current_point >= r_background:
                current_point -= r_background
            else:
                current_point = 0.0

        t_p.append((current_point, float(data_set[0][6][index]), float(data_set[0][7][index])))

subtract_background(data_glass)
