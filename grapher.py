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
                data_air[file_count][0].append([line[0]])
                data_air[file_count][1].append([line[1]])
                data_air[file_count][2].append([line[2]])
                data_air[file_count][3].append([line[3]])
                data_air[file_count][4].append([line[4]])
                data_air[file_count][5].append([line[5]])
                data_air[file_count][6].append([line[6]])
                data_air[file_count][7].append([line[7]])
                data_air[file_count][10].append([line[10]])
            elif line != []:
                data_glass[file_count][0].append([line[0]])
                data_glass[file_count][1].append([line[1]])
                data_glass[file_count][2].append([line[2]])
                data_glass[file_count][3].append([line[3]])
                data_glass[file_count][4].append([line[4]])
                data_glass[file_count][5].append([line[5]])
                data_glass[file_count][6].append([line[6]])
                data_glass[file_count][7].append([line[7]])
                data_glass[file_count][10].append([line[10]])
    file_count += 1
