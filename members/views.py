from datetime import datetime
from datetime import date
import time
import csv
import json

# SEE: http://www.traddicts.org/webdevelopment/flexible-and-simple-json-serialization-for-django/ 
from fix_json import JSONSerializer

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseNotFound

from members.models import Member, Tournament

from IPython import embed

def index(request):
    tournament = Tournament.objects.all()[0]
    return render_to_response('index.html', {'title': tournament.title, 'logo_url': tournament.logo.url }, context_instance=RequestContext(request))

def query_all(request):
    ip_addr = request.META['REMOTE_ADDR']
    m_all = Member.objects.all()
    jsonSerializer = JSONSerializer()
    data = jsonSerializer.serialize({'aaData': m_all})
    print "%s : query_all" % ip_addr

    return HttpResponse(data, mimetype="application/json")

TOP5_LIST = []
def query_dojo(request):
    m_all = Member.objects.all()
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
    data_list = []
    for key, val in dojo_dict.iteritems():
        data_list.append({'dojo': key, 'score': val})
    global TOP5_LIST
    TOP5_LIST = []
    TOP5_LIST = data_list

    jsonSerializer = JSONSerializer()
    data = jsonSerializer.serialize({'aaData': data_list })

    return HttpResponse(data, mimetype="application/json")

def query_top5(request):
    query_dojo(request)
    global TOP5_LIST
    dojo_list = TOP5_LIST
    dojo_list.sort(key=lambda item: item['score'], reverse=True)
    top5_list = dojo_list[:5]
    data_object = {'dojo': [], 'score': []}
    for o in top5_list:
        data_object['dojo'].append(o['dojo'])
        data_object['score'].append(o['score'])

    print data_object
    s = data_object['score']
    jsonSerializer = JSONSerializer()
    data = jsonSerializer.serialize({'dojo': data_object['dojo'], 'score': str(s)})
    return HttpResponse(data, mimetype="application/json")

def query_completed(request):
    m_all = Member.objects.all()
    total_member = len(m_all)
    completed = 0
    for m in m_all:
        if len(m.place) > 0:
            completed += 1
    completed_percentage = float(completed) / float(total_member)
    completed_percentage = int( round(completed_percentage, 2) * 100 )
    not_completed_percentage = 100 - completed_percentage
    data_object = {'percent': [ ['Completed', completed_percentage], ['Not Completed', not_completed_percentage] ]}

    jsonSerializer = JSONSerializer()
    data = jsonSerializer.serialize(data_object)
    return HttpResponse(data, mimetype="application/json")

def query_member(request, pk):
    try: 
        member = Member.objects.filter(pk=pk)[0]
    except IndexError: 
        error_msg = 'Cannot find the member.'
        return render_to_response('member.html', {'error_msg': error_msg }, context_instance=RequestContext(request))
    is_checked = member.check_in
    weight = member.weight
    data = {
        'name': member,
        'isChecked': is_checked,
        'weight': weight
    }
    return render_to_response('member.html', data, context_instance=RequestContext(request))

@login_required
def check_in_member(request, pk):
    if request.method == 'POST':
        try: 
            member = Member.objects.filter(pk=pk)[0]
        except IndexError: 
            return HttpResponse(HttpResponseNotFound)
        member.check_in = True
        member.save()
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@login_required
def weight_in_member(request, pk):
    pass
