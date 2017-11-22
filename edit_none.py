import csv

new_file = open('sample_data/rain/5-9_2017_edit_none.csv','w')
data_file = open('sample_data/rain/5-9_2017.csv','r')
data = csv.reader(data_file)
i = 0
for row in data:
    if row[3] == 'None':
        row[3] = '-1'
    
    new_file.write(row[0] + ',' + row[1] + ',' + row[2] + ',' + row[3] + '\n')