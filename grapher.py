import os, csv
from pprint import pprint
import matplotlib.pyplot as plt

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

    def _convert(volt_index, background, second_theta_val, array_to_use):
        # Data points daved will be in tuple (data, theta 1, [thea 2 if T, theta 3 if R])
        for index, r_s_val in enumerate(data_set[0][volt_index]):
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
                if current_point >= background:
                    current_point -= background
                else:
                    current_point = 0.0

            try:
                second_theta = float(data_set[0][second_theta_val][index])
                if second_theta < 0.0:
                    second_theta = 360.0 - second_theta
            except:
                second_theta = 999

            print("Theta 1")
            print(float(data_set[0][6][index]))

            array_to_use.append((current_point, float(data_set[0][6][index]), second_theta))

    _convert(0, t_background, 7, t_p)
    _convert(1, t_background, 7, t_s)
    _convert(3, r_background, 10, r_p)
    _convert(4, r_background, 10, r_s)

    return t_p, t_s, r_p, r_s

glass_t_p, glass_t_s, glass_r_p, glass_r_s = subtract_background(data_glass)
air_t_p, air_t_s, air_r_p, air_r_s = subtract_background(data_air)

# Now start graphing: (R/T vs Theta 1, or all vs the angle)

def plot_vs_angle(tuples):
    angle = []
    value = []
    for element in tuples:
        print("Theta 1")
        print(element[1])
        value.append(element[0])
        angle.append(element[1])
    plt.scatter(angle, value)

#plot_vs_angle(glass_r_p)
#plot_vs_angle(glass_r_s)
plot_vs_angle(glass_t_p)
#plot_vs_angle(glass_t_s)
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.show()