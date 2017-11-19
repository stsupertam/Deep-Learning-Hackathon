import csv

with open('data/rain/station.csv', 'w') as file:
    with open('data/rain/5-9_2017.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        w = []
        i = 0
        station = 0
        for row in reader:
            w.append(row[1])
            if(i != 0):
                if(w[i-1] != w[i]):
                    station += 1
                    file.write(str(station) + ',' + row[1] + ',' + row[2] + '\n')
            else:
                file.write(str(station) + ',' + row[1] + ',' + row[2] + '\n')
            i += 1
        print(station)