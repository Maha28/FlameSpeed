from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import render
import models
import pdb

def home(request):
    return render(request, 'home.html')

def database(request):
    return render(request, 'database.html') 

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
            mixture_instance['references'] = mixture_instance['references'] + str(reference.id_ref)
        mixtures.append(mixture_instance)
    context['mixtures'] = mixtures
    return render(request, 'mixture.html',context) 

def graph(request): 
    context = {}
    mixtures  = list()
    for mixture in models.Mixture.objects.all():
        mixture_instance = {}
        mixture_instance['references'] = ''
        mixture_instance['name'] = mixture.name
        for reference in mixture.references.all():
            mixture_instance['references'] = mixture_instance['references'] + str(reference.id_ref)
        mixtures.append(mixture_instance)
    context['mixtures'] = mixtures
    return render(request, 'graph.html',context)

def search(request):
    context = {}
    mixtures  = list()
    for mixture in models.Mixture.objects.all():
        mixtures.append(mixture.name)
    context['mixtures'] = mixtures

    characteristics  = list()
    for characteristic in models.Characteristic.objects.all():
        characteristics.append(characteristic.name)
    context['characteristics'] = list(set(characteristics))
    
    references  = list()
    for reference in models.Reference.objects.all():
        references.append(reference.id_ref)
    context['references'] = references

    if request.method == 'POST':
         context['mixture']=models.Mixture.objects.filter(name = request.POST['mixture'])
         context['characteristic']=models.Characteristic.objects.filter(name = request.POST['characteristic'])
         context['reference']=models.Reference.objects.filter(id_ref = request.POST['reference'])
         messages.success(request, "You have successfully submited your search")
    return render(request, 'search.html', context)

def Result_search(request): 
    return render(request, 'Result_search.html',context)

def database_search(request):
    context = {}
    context['database_search'] = models.Mixture.objects.all() 
    return render(request, 'database_search.html',context)    

def H2_air(request):
    context = {}
    characteristic_list  = list()
    for characteristic in models.Characteristic.objects.filter(mixture = 'H2_air'):
        characteristic_list.append(characteristic.name)
    context['characteristic_list'] = list(set(characteristic_list))
    return render(request, 'H2_air.html', context) 

def H2_air_steam(request):
    return render(request, 'H2_air_steam.html') 

def H2_CO(request):
    return render(request, 'H2_CO.html')

def H2_air_CO(request):
    return render(request, 'H2_air_CO.html') 

def H2_O2(request):
    return render(request, 'H2_O2.html')

def H2_air_CO2(request):
    return render(request, 'H2_air_CO2.html')

def H2_air_CO_CO2(request):
    return render(request, 'H2_air_CO_CO2.html') 

def H2_air_Pressure(request):
    return render(request, 'H2_air_Pressure.html') 

def H2_air_Pressure_Ref1(request):
    context = {}
    context['data'] = models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2_air')   
    return render(request, 'H2_air_Pressure_Ref1.html',context)

def H2_air_CO_Pressure(request):
    return render(request, 'H2_air_CO_Pressure.html') 

def H2_air_equivalence_ratio(request):
    context = {}
    reference_list  = list()
    context['characteristic']=models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2_air')
    for reference in models.Reference.objects.all():
        reference_list.append(reference.id_ref)
    context['reference_list'] = list(set(reference_list))
    return render(request, 'H2_air_equivalence_ratio.html', context)

def populate_reference (request):
    models.Reference.objects.populate_reference() 
    return HttpResponseRedirect(reverse('reference'))

def populate_mixture_characteristic (request):
    models.Mixture.objects.populate_mixture_characteristic() 
    return HttpResponseRedirect(reverse('mixture')) 
        