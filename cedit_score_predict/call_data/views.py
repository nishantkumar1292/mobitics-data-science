from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.conf import settings

from .forms import ParamsForm

import os
import json
import math

# Create your views here.
class HomePageView(TemplateView):
    """docstring for HomePageView."""
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

class ParamsPageView(TemplateView):
    template_name = "params.html"

def get_params(request):
    if request.method == 'POST':
        form = ParamsForm(request.POST)
        if form.is_valid():
            incoming = form.cleaned_data['incoming_calls']
            outgoing = form.cleaned_data['outgoing_calls']
            missed = form.cleaned_data['missed_calls']
            blank = form.cleaned_data['blank_calls']
            all_calls = incoming + outgoing + missed + blank

            #calculating fractions
            calls = [incoming, outgoing, missed, blank]
            inputVector = [x/all_calls for x in calls]
            result = predict(inputVector)
            print ('result: '+result)
            if result == '1.0':
                person = 'GOOD'
            else:
                person = 'BAD'

            return render_to_response('predictions.html', {'person_type': person})
    else:
        form = ParamsForm()
    return render(request, 'params.html', {'form': form})

def predict(inputVector):
    summaries = get_summaries()
    probablities = calculateClassProbablities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probablity in probablities.items():
        if bestLabel is None or probablity > bestProb:
            bestProb = probablity
            bestLabel = classValue
    return bestLabel

def get_summaries():
    filename = os.path.join(settings.BASE_DIR, 'call_data/data/output.json')
    with open(filename) as data:
        summaries = json.load(data)
        return summaries

def calculateClassProbablities(summaries, inputVector):
    probablities = {}
    for classValue, classSummaries in summaries.items():
        probablities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probablities[classValue] *= calculateProbablity(x, mean, stdev)
    return probablities

def calculateProbablity(x, mean, stdev):
	exponent = math.exp(-(math.pow(x-mean,2))/(2*math.pow(stdev,2)))
	return (1/(math.sqrt(2*math.pi)*stdev))*exponent
