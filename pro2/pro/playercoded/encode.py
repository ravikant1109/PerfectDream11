import csv

with open("out.csv", 'r') as input, open('temp.csv', 'w') as output:
    reader = csv.reader(input, delimiter = ',')
    writer = csv.writer(output, delimiter = ',')

    all = []
    row = next(reader)
    row.insert(0, 0)
    all.append(row)
    count = 0
    for row in reader:
        count += 1
        row.insert(0, count)
        all.append(row)
    writer.writerows(all)