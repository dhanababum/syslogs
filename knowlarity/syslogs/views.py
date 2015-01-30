from django.shortcuts import render, HttpResponse

from .models import Occurence

import json


def json_wraper(log):
    """
      model object to json dictionary
      Parms: model objects
    """
    return {
        'id': "%s" % log.id,
        'updated_date': log.updated_date,
        'occured': log.occured,
        'programme': log.programme}


def system_log(request):
    logs = Occurence.objects.all()
    return render(request, 'syslogs/programmes.html', {'logs': logs})


def new_logs(request):
    api = {}
    api['success'] = False
    if request.method == 'POST':
        api['success'] = True
        date = request.POST.get('date')
        logs = Occurence.objects.filter(updated_date__gt=int(date))
        api['logs'] = [json_wraper(log) for log in logs]
    return HttpResponse(json.dumps(api))
