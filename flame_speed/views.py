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

#def database(request):
#    return render(request, 'database.html') 

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
         selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
         selected_reference = models.Reference.objects.get(id_ref = request.POST['reference'])
         search = models.Characteristic.objects.filter(mixture = selected_mixture).filter(reference = selected_reference).filter(name=request.POST['characteristic']).filter()
         context['results'] = search
         messages.success(request, "You have successfully submitted your search")
    return render(request, 'search.html', context)

def Result_search(request): 
    return render(request, 'Result_search.html',context)   

#Templates
def H2(request):
    context = {}
    characteristic_list  = list()
    for characteristic in models.Characteristic.objects.filter(mixture = 'H2'):
        characteristic_list.append(characteristic.name)
    context['characteristic_list'] = list(set(characteristic_list))
    return render(request, 'H2.html', context) 

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

def H2_Pressure_Ref1(request):
    context = {}
    context['data'] = models.Characteristic.objects.filter(name = 'equivalence_ratio', mixture ='H2')   
    return render(request, 'H2_Pressure_Ref1.html',context)

def H2_air_CO_Pressure(request):
    return render(request, 'H2_air_CO_Pressure.html') 

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

def database(request):
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
            
            return render(request, 'database.html',context) 
        #case 2: mixture and characteristic were selected
        elif 'mixture' in request.POST and 'characteristic' in request.POST and not 'reference' in request.POST  :
            selected_mixture = models.Mixture.objects.get(name = request.POST['mixture'])
            selected_characteristics = models.Characteristic.objects.filter(mixture = selected_mixture, name = request.POST['characteristic'])
            reference_list  = list()
            for characteristic in selected_characteristics:
                reference_list.append(characteristic.reference.id_ref)
            context['reference_list'] = list(set(reference_list))
            
            mix_name = list()
            mix_name.append(selected_mixture.name)
            context['mixtures'] = mix_name        
            
    #        charact_name = list()
    #        charact_name.append(models.Characteristic.objects.filter(name = request.POST['characteristic'])) 
    #        context['characteristic_list'] = set(charact_name)
            
            return render(request, 'database.html',context)
    else:
        mixtures  = list()
        for mixture in models.Mixture.objects.all():
            mixtures.append(mixture.name)
        context['mixtures'] = mixtures
        
    return render(request, 'database.html',context)
