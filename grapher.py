import os, csv
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter

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
            if dataset == 'data1.csv' and line != []:
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
        baseline = 0.0
        # get baseline for other things
        print(data_set[0][volt_index])
        for r_s_val in data_set[0][volt_index]:
            current_val = 0.0
            if r_s_val != '':
                print(r_s_val)
                if float(r_s_val) <= 10.0:
                    current_val = float(r_s_val)*1000.0
                    print(current_val)
                else:
                    current_val = float(r_s_val)
                if current_val > baseline:
                    baseline = current_val
        print("Baseline")
        print(baseline)

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
            if baseline != 0.0:
                current_point /= baseline

            try:
                second_theta = float(data_set[0][second_theta_val][index])
                if second_theta < 0.0:
                    second_theta = 360.0 - second_theta
            except:
                second_theta = 999

            array_to_use.append((current_point, float(data_set[0][6][index]), second_theta))

    _convert(0, t_background, 7, t_p)
    _convert(1, t_background, 7, t_s)
    _convert(3, r_background, 10, r_p)
    _convert(4, r_background, 10, r_s)


    return t_p, t_s, r_p, r_s

glass_t_p, glass_t_s, glass_r_p, glass_r_s = subtract_background(data_glass)
air_t_p, air_t_s, air_r_p, air_r_s = subtract_background(data_air)

# Now start graphing: (R/T vs Theta 1, or all vs the angle)

def plot_vs_angle(tuples, label):
    angle = []
    value = []
    for element in tuples:
        if float(element[0]) != 0.0 and element[1] not in angle:
            print(element[0])
            value.append(element[0])
            angle.append(element[1])
    plt.scatter(angle, value, label=label)

def plot_ratio(tuple1, tuple2, label):
    angle = [0.0]
    value = [0.0]
    for index, element in enumerate(tuple1):
        if float(element[0]) != 0.0 and float(tuple2[index][0]) != 0.0 and element[1] not in angle:
            value.append(element[0]/tuple2[index][0])
            angle.append(element[1])
    #angle = angle[:-1]
    #value = value[:-1]
    plt.scatter(angle, value, label=label)
    print(angle)
    if angle != [0.0]:
        xp = np.linspace(0, max(angle)+10, 100)
        z = np.polyfit(angle, value, 2)
        yp = z[0]*xp**4 + z[1]*xp**3 + z[2]*xp**1 + z[2]
        yp1 = 1 - yp
        plt.plot(xp, yp)
        plt.plot(xp, yp1)

def plot_theory(theta1, theta2):
    glass_n = 1.5
    air_n = 1.0

    r_p = (np.tan((theta1 - theta2)**2)/(np.tan((theta1+theta2))**2))
    t_p = (2*np.cos(theta1)*np.sin(theta2))/(np.sin((theta1+theta2))*np.cos((theta1-theta2)))
    r_s = (np.sin((theta1 - theta2))**2/(np.sin((theta1+theta2)))**2)
    t_s = (np.sin(2*theta1)*np.sin(2*theta2))/(np.sin((theta1+theta2))**2)

    p_polarixed = r_p/t_p
    s_polarized = r_s/t_s

    plt.plot(theta1, p_polarixed)
    plt.plot(theta1, s_polarized)

def plot_i_frac(tuples, label):
    angle = []
    value = []
    for element in tuples:
        if float(element[0]) != 0.0 and element[1] not in angle:
            print(element[0])
            value.append(element[0])
            angle.append(element[1])
    if angle != []:
        xp = np.linspace(0, max(angle) + 10, 100)
        z = np.polyfit(angle, value, 2)
        yp = z[0] * xp ** 2 + z[1] * xp ** 1 + z[2]
        yp1 = 1 - yp
        plt.plot(xp, yp)
    plt.scatter(angle, value, label=label)

# sin(theta incidence)/sin(theta reflection) = n

def snell(reflection, n):
    # assumes that n is 1 for air
    theta = np.arcsin(n*np.sin(reflection))
    return theta



theta1 = np.arange(0, 100, step=5)
theta3 = np.arange(160, 0, step=-8)
theta2 = np.arange(0, -40, step=-2)
theta2_pos = np.arange(0, 40, step=2)

plot_i_frac(glass_r_p, "Rp")
plot_i_frac(glass_r_s, "Rs")
plot_i_frac(glass_t_p, "Tp")
plot_i_frac(glass_t_s, "Ts")
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.title("Air to Glass")
plt.legend(loc=0)
plt.show()

plot_vs_angle(glass_r_p, "Rp")
plot_vs_angle(glass_r_s, "Rs")
plot_vs_angle(glass_t_p, "Tp")
plot_vs_angle(glass_t_s, "Ts")
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.title("Air to Glass")
plt.legend(loc=0)
plt.ylim([0,1])
plt.show()

plot_ratio(glass_r_p, glass_t_p, "Rp/Tp")
plot_ratio(glass_r_s, glass_t_s, "Rs/Ts")
#plot_theory(theta1, theta1)
plt.title("Air to Glass")
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.ylim([0,1])
plt.legend(loc=0)
plt.show()

plot_vs_angle(air_r_p, "Rp")
plot_vs_angle(air_r_s, "Rs")
plot_vs_angle(air_t_p, "Tp")
plot_vs_angle(air_t_s, "Ts")
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.title("Glass to Air")
plt.legend(loc=0)
plt.show()

#plot_theory(theta1, theta3)
plot_ratio(air_r_p, air_t_p, "Rp/Tp")
plot_ratio(air_r_s, air_t_s, "Rs/Ts")
plt.title("Glass to Air")
plt.ylabel("R/T")
plt.xlabel("Theta 1")
plt.ylim([0,1])
plt.legend(loc=0)
plt.show()

# Glass-Air: Theta2 = angle of glass + photodetector
def plot_sins(data_set, label):
    angle_1 = []
    angle_2 = []
    for element in data_set:
        if float(element[0]) != 0.0 and element[1] not in angle_1 and element[2] != 999:
            angle_1.append(np.sin(np.deg2rad(element[1])))
            angle_2.append(np.sin(np.deg2rad(element[1] + element[2])))
    plt.plot(angle_1, angle_2, label=label)
    np_angle1 = np.asarray(angle_1)
    np_angle2 = np.asarray(angle_2)
    n = np_angle1/np_angle2
    print("N " + str(label))
    print(n)

plot_sins(air_r_p, "Rp")
plot_sins(air_r_s, "Rs")
#plot_sins(air_t_p, "Tp")
plot_sins(air_t_s, " Air Ts")
plot_sins(glass_r_p, "Glass Rp")
#plot_sins(glass_r_s, "Rs")
plot_sins(glass_t_p, "Glass Tp")
plot_sins(glass_t_s, "Ts")
plt.ylabel("Sin(Theta 1)")
plt.xlabel("Sin(Theta 2)")
plt.legend(loc=0)
plt.show()