from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render
import models
import pdb
import json

#Populates
def populate_reference (request):
    models.Reference.objects.populate_reference() 
    return HttpResponseRedirect(reverse('reference'))

def populate_mixture_characteristic (request):
    models.Mixture.objects.populate_mixture_characteristic() 
    return HttpResponseRedirect(reverse('mixture')) 

#Base
def home(request):
    return render(request, 'home.html')

def mixture(request):
    context = {}
    mixtures  = list()
    for mixture in models.Mixture.objects.all():
        mixture_instance = {}
        mixture_instance['references'] = ''
        mixture_instance['name'] = mixture.name
        for reference in mixture.references.all():
            mixture_instance['references'] = mixture_instance['references'] +str(reference.id_ref)+","
        mixtures.append(mixture_instance)
    context['mixtures'] = mixtures
    return render(request, 'mixture.html',context) 

def characteristic(request):
    context = {}
    context['characteristics'] = models.Characteristic.objects.all() 
    return render(request, 'characteristic.html',context) 

def reference(request):
    context = {}
    context['reference'] = models.Reference.objects.all() 
    context['range'] = range(1,16)
    return render(request, 'reference.html',context) 

def data(request):
    context = {}

    if request.method == 'POST':
        #case 1: only mixture was selected
        if 'mixture' in request.POST and not 'characteristic' in request.POST and not 'pressure_max' in request.POST and not 'pressure_min' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            characteristic_list  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture):
                characteristic_list.append(characteristic.name) 
            context['characteristic_list'] = list(set(characteristic_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name
            
            return render(request, 'data.html',context) 
        
        #case 2: mixture, characteristic were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'pressure_max' in request.POST  and not 'pressure_min' in request.POST :    
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])                          
            selected_characteristics = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture = selected_mixture)         
            
            charact_name = list() 
            for characteristic in selected_characteristics:
                charact_name.append(characteristic.name)
            context['characteristic_list'] = list(set(charact_name))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 

            return render(request, 'data.html',context)
              
        #case 3: mixture, characteristic and pressure were selected 
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'pressure_max' in request.POST and 'pressure_min' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(mixture = selected_mixture, name = request.POST['characteristic'], pressure_range = ['pressure_min','pressure_max'])
            context['data'] =  selected_characteristics
            
        return render(request, 'data.html',context)
    
    else:
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'data.html',context)


def graph(request):
    context = {}

    if request.method == 'POST':
        #case 1: mixture were selected
        if 'mixture' in request.POST and not 'characteristic' in request.POST:
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            characteristic_list  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture):
                characteristic_list.append(characteristic.name) 
            context['characteristic_list'] = list(set(characteristic_list))
          
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name

            return render(request, 'graph.html',context) 
        
        #case 2: mixture, characteristic were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'press_temp' in request.POST :    
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])                          
            selected_characteristics = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture = selected_mixture) 
            
            press_temp_list  = list()
            charact_name = list() 
            for characteristic in selected_characteristics:
                press_temp_list.append(characteristic.press_temp)
                charact_name.append(characteristic.name)
            context['press_temp_list'] = list(set(press_temp_list))
            context['characteristic_list'] = list(set(charact_name))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name     
            
            return render(request, 'graph.html',context)
        
        #case 3: mixture, characteristic and press_temp were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'press_temp' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(mixture = selected_mixture, name = request.POST['characteristic'], press_temp = request.POST['press_temp'])
            charact = request.POST['characteristic']
            
            return render(request, 'display_graph.html', {'results':selected_characteristics,'charact':charact})

    else:        
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'graph.html',context)

#Templates
def display_graph(request):
    return render(request, 'display_graph.html',context)