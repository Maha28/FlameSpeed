from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render
import models
import pdb

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

def characteristic(request):
    context = {}
    context['characteristics'] = models.Characteristic.objects.all() 
    return render(request, 'characteristic.html',context) 

def reference(request):
    context = {}
    context['reference'] = models.Reference.objects.all() 
    context['range'] = range(1,16)
    return render(request, 'reference.html',context) 

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
            
            context['characteristic_list'] = list(set(charact_name))
            
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
            context['data'] = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture =request.POST['mixture'], reference = request.POST['reference'], conditions = request.POST['conditions'])            
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
            
            return render(request, 'graph.html',context) 
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
            
            context['characteristic_list'] = list(set(charact_name))
            
            return render(request, 'graph.html',context)
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
            
            return render(request, 'graph.html',context)
        
        #case 4: mixture,characteristic, reference and conditions were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'reference' in request.POST and 'conditions' in request.POST :
            context['characteristic_name'] = request.POST['characteristic']
            context['data'] = models.Characteristic.objects.filter(name = request.POST['characteristic'], mixture =request.POST['mixture'], reference = request.POST['reference'], conditions = request.POST['conditions'])            
            return render(request, 'display_graph.html',context)
    else:
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'graph.html',context)

#Templates
def H2(request):
    context = {}
    characteristic_list  = list()
    for characteristic in models.Characteristic.objects.filter(mixture = 'H2'):
        characteristic_list.append(characteristic.name)
    context['characteristic_list'] = list(set(characteristic_list))
    return render(request, 'H2.html', context) 

def H2_equivalence_ratio(request):
    context = {}
    reference_list  = list()
    selected_characteristic=models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2')
    for characteristic in selected_characteristic:
        reference_list.append(characteristic.reference)
    context['reference_list'] = list(set(reference_list))
    return render(request, 'H2_equivalence_ratio.html', context)

def H2_equivalence_ratio_ref6(request):
    context = {}
    context['data'] = models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2', conditions = 'P=0.35atm,T=25C', reference = '6')   
    context['data1'] = models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2', conditions = 'P=0.5atm,T=25C', reference = '6')
    return render(request, 'H2_equivalence_ratio_ref6.html',context)

def display_graph(request):
    return render(request, 'display_graph.html',context)