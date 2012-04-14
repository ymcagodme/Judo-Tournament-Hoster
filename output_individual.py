from members.models import Member
import csv

file = open('output_individual.csv', 'wb')
w = csv.writer(file, dialect='excel')

m_all = Member.objects.all()
HEADER = ['First Name', 'Last Name', 'Dojo Title', 'Gender', 'Age', 'Place']
w.writerow(HEADER)
for m in m_all:
    row = []
    row.append(m.first_name)
    row.append(m.last_name)
    row.append(m.dojo)
    row.append(m.gender)
    row.append(m.age)
    row.append(m.place)
    print row
    w.writerow(row)

file.close()
