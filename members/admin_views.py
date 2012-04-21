import csv

from members.models import Member
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def gen_dojo_result(request):
    file = open('output_dojo.csv', 'wb')
    w = csv.writer(file, dialect='excel')

    m_all = Member.objects.all()
    HEADER = ['Dojo Title', 'Score']
    w.writerow(HEADER)
    dojo_dict = {}
    for m in m_all:
        if dojo_dict.has_key(m.dojo) is False:
            dojo_dict[m.dojo] = 0
        if m.place == '1st':
            score = 5
        elif m.place == '2nd':
            score = 3
        elif m.place == '3rd':
            score = 1
        else:
            score = 0
        dojo_dict[m.dojo] += score

    for key, val in dojo_dict.iteritems():
        row = []
        row.append(key)
        row.append(val)
        w.writerow(row)

    file.close()

@staff_member_required
def echo(request):
    return HttpResponse('Got it')

@staff_member_required
def add_multiple_matches(request):
    return render_to_response('admin/members/match/add_multiple_matches.html', {}, RequestContext(request, {}) )
