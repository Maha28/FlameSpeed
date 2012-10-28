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
        if 'mixture' in request.POST and not 'characteristic' in request.POST and not 'reference' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            characteristic_list  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture):
                characteristic_list.append(characteristic.name) 
            context['characteristic_list'] = list(set(characteristic_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name
            
            return render(request, 'data.html',context) 
        #case 2: mixture and characteristic were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'reference' in request.POST and not 'conditions' in request.POST :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(mixture = selected_mixture, name = request.POST['characteristic'])
            reference_list  = list()
            charact_name = list() 
            for characteristic in selected_characteristics:
                reference_list.append(characteristic.reference.id_ref)
                charact_name.append(characteristic.name)
            context['reference_list'] = list(set(reference_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name        
            
#            context['characteristic_list'] = list(set(charact_name))
            context['data'] = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture =request.POST['mixture'])
            
            return render(request, 'data.html',context)
        #case 3: mixture,characteristic and reference were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'reference' in request.POST and not 'conditions' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(mixture = selected_mixture, name = request.POST['characteristic'], reference = request.POST['reference'])
            conditions_list  = list()
            charact_name = list() 
            for characteristic in selected_characteristics:
                conditions_list.append(characteristic.conditions)
                charact_name.append(characteristic.name)
            context['conditions_list'] = list(set(conditions_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name                   
            context['characteristic_list'] = list(set(charact_name))
            ref_list = list()
            ref_list.append(request.POST['reference'])
            context['reference_list'] = list(set(ref_list))
            
            return render(request, 'data.html',context)
        
        #case 4: mixture,characteristic, reference and conditions were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'reference' in request.POST and 'conditions' in request.POST :
            context['characteristic_name'] = request.POST['characteristic']   
#            context['data'] = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture =request.POST['mixture'], reference = request.POST['reference'], conditions = request.POST['conditions'])          
            return render(request, 'data.html', context)
    else:
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'data.html',context)


def graph(request):
    context = {}

    if request.method == 'POST':
        #case 1: mixture1 were selected
        if 'mixture1' in request.POST and not 'characteristic1' in request.POST:
            selected_mixture1 = models.Mixture.objects.get(name = request.POST['mixture1'])
            characteristic_list1  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture1):
                characteristic_list1.append(characteristic.name) 
            context['characteristic_list1'] = list(set(characteristic_list1))
          
            mix_name1 = list()
            mix_name1.append(selected_mixture1.name)
            context['mixtures1'] = mix_name1

            return render(request, 'graph.html',context) 
        
        #case 2': mixture1, characteristic1 were selected
        elif 'mixture1' in request.POST and 'characteristic1' in request.POST:    
            selected_mixture1 = models.Mixture.objects.get(name = request.POST['mixture1'])                          
            selected_characteristics = models.Characteristic.objects.filter(name = request.POST['characteristic1'], mixture = selected_mixture1)       
                    
            charact = request.POST['characteristic1']
            return render(request, 'display_graph.html', {'results':selected_characteristics,'charact':charact})
        
    else:        
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures1'] = mixtures
        
    return render(request, 'graph.html',context)

#Templates
def display_graph(request):
    return render(request, 'display_graph.html',context)