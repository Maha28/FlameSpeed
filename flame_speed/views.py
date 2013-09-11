from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render
from itertools import chain
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
    graph={}
    global selected_characteristics1
    selected_characteristics1 = []
    global selected_characteristics2
    selected_characteristics2 = []
    if request.method == 'POST':
        #case 1: only mixture was selected
        if 'mixture' in request.POST and not 'characteristic' in request.POST:
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            characteristic_list  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture):
                characteristic_list.append(characteristic.name) 
            characteristic_list.append('Pressure')
            characteristic_list.append('Temperature')
            
            context['characteristic_list'] = list(set(characteristic_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name
            
            return render(request, 'data.html',context) 
        
        #case 2: mixture, characteristic were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'nN2_nO2' in request.POST and request.POST['pressure_min'] == "" and request.POST['pressure_max'] == "" and request.POST['temperature_min'] == "" and request.POST['temperature_max'] == "":    
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])                           
            selected_characteristics = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'])
            
            charact_name = list()           
            for characteristic in selected_characteristics:
                charact_name.append(characteristic.name)
            context['characteristic_list'] = list(set(charact_name))
                        
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 
            

            return render(request, 'data.html',context)
        
        #case 3: mixture, characteristic, oxydant  were selected  
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'nN2_nO2' in request.POST and request.POST['pressure_min'] == "" and request.POST['pressure_max'] == "" and request.POST['temperature_min'] == "" and request.POST['temperature_max'] == "":            
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(nN2_nO2 = request.POST['nN2_nO2'], mixture = request.POST['mixture'], name = request.POST['characteristic'])
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 
            
            charact_name = list()           
            charact_name.append(request.POST['characteristic'])
            context['characteristic_list'] = charact_name            
            
            return render(request, 'data.html',context)  
        
        #case 4: mixture, characteristic, oxydant, temperature and pressure were selected  
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'nN2_nO2' in request.POST and 'pressure_min' in request.POST and 'pressure_max' in request.POST and 'temperature_min' in request.POST and 'temperature_max' in request.POST : 
            temperature_min = request.POST['temperature_min']
            temperature_max = request.POST['temperature_max']
            pressure_min = request.POST['pressure_min']
            pressure_max = request.POST['pressure_max']
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 
            
            charact_name = list()           
            charact_name.append(request.POST['characteristic'])
            context['characteristic_list'] = charact_name 
            
            if (request.POST['characteristic']== 'Pressure' ):
                selected_characteristics1 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], value__range= [float(pressure_min),float(pressure_max)], temperature__range=[temperature_min,temperature_max])         
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])
            elif (request.POST['characteristic']== 'Temperature' ):
                selected_characteristics1 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], value__range=[float(temperature_min),float(temperature_max)])
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])            
            else:
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])
                 
            selected_characteristics = sorted(chain(selected_characteristics1, selected_characteristics2))
            
            context['data'] = selected_characteristics
            
            return render(request, 'display_data.html',context) 

#           for record in selected_characteristics:
#                if (graph[record.reference.source, record.pressure, record.temperature, record.CO, record.CO2, record.H2O, record.N2, record.details] == null):                
#                    graph["{{record.reference.source}}, {{record.pressure}}, {{record.temperature}}, {{record.CO}}, {{record.CO2}}, {{record.H2O}}, {{record.N2}}, {{record.details}}"] = []
#                else:
#                    graph["{{record.reference.source}}, {{record.pressure}}, {{record.temperature}}, {{record.CO}}, {{record.CO2}}, {{record.H2O}}, {{record.N2}}, {{record.details}}"].append( [ {{record.value}} , {{record.speed}}] )

#        return render(request, 'data.html',{'data':selected_characteristics,'data_organised':graph})'''

    else:
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'data.html',context)


def graph(request):
    context = {}
    global selected_characteristics1
    selected_characteristics1 = []
    global selected_characteristics2
    selected_characteristics2 = []

    if request.method == 'POST':
        #case 1: mixture were selected
        if 'mixture' in request.POST and not 'characteristic' in request.POST:
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            characteristic_list  = list()
            for characteristic in models.Characteristic.objects.filter(mixture = selected_mixture):
                characteristic_list.append(characteristic.name) 
            characteristic_list.append('Pressure')
            characteristic_list.append('Temperature')
            
            context['characteristic_list'] = list(set(characteristic_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name

            return render(request, 'graph.html',context) 
        
        #case 2: mixture, characteristic were selected            
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'nN2_nO2' in request.POST and request.POST['pressure_min'] == "" and request.POST['pressure_max'] == "" and request.POST['temperature_min'] == "" and request.POST['temperature_max'] == "":    
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])                           
            selected_characteristics = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'])
            
            charact_name = list()           
            for characteristic in selected_characteristics:
                charact_name.append(characteristic.name)
            context['characteristic_list'] = list(set(charact_name))
                        
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name             

            return render(request, 'graph.html',context)
        
        #case 3: mixture, characteristic and pressure were selected            
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'nN2_nO2' in request.POST and request.POST['pressure_min'] == "" and request.POST['pressure_max'] == "" and request.POST['temperature_min'] == "" and request.POST['temperature_max'] == "":            
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(nN2_nO2 = request.POST['nN2_nO2'], mixture = request.POST['mixture'], name = request.POST['characteristic'])
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 
            
            charact_name = list()           
            charact_name.append(request.POST['characteristic'])
            context['characteristic_list'] = charact_name   
            
            return render(request, 'graph.html',context)
        
        
        #case 4: mixture, characteristic,pressure and temperature were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and 'nN2_nO2' in request.POST and 'pressure_min' in request.POST and 'pressure_max' in request.POST and 'temperature_min' in request.POST and 'temperature_max' in request.POST : 
            temperature_min = request.POST['temperature_min']
            temperature_max = request.POST['temperature_max']
            pressure_min = request.POST['pressure_min']
            pressure_max = request.POST['pressure_max']
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name 
            
            charact_name = list()           
            charact_name.append(request.POST['characteristic'])
            context['characteristic_list'] = charact_name 
            
            if (request.POST['characteristic']== 'Pressure' ):
                selected_characteristics1 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], value__range= [float(pressure_min),float(pressure_max)], temperature__range=[temperature_min,temperature_max])         
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])
            elif (request.POST['characteristic']== 'Temperature' ):
                selected_characteristics1 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], value__range=[float(temperature_min),float(temperature_max)])
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])            
            else:
                selected_characteristics2 = models.Characteristic.objects.filter(mixture = request.POST['mixture'], name = request.POST['characteristic'], nN2_nO2 = request.POST['nN2_nO2'], pressure__range= [pressure_min,pressure_max], temperature__range=[temperature_min,temperature_max])
                 
            selected_characteristics = sorted(chain(selected_characteristics1, selected_characteristics2))      
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

def display_data(request):
    return render(request, 'display_data.html',context)