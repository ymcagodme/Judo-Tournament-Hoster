from members.models import Member
import csv

file = open('data.csv', 'rb')
reader = csv.reader(file)

for l in reader:
    new_member = Member.objects.create(user_id=1, first_name=l[0], last_name=l[1])
    new_member.dojo = l[2]
    new_member.gender = l[3]
    new_member.age = l[4]
    new_member.user_id = 1
    new_member.save()

file.close()
