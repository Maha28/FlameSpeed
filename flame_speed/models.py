from django.db import models
import glob, os, pdb
PROJECT_PATH = "/home/maha/workspace/FlameSpeed/Data/"
RefFile_PATH = "/home/maha/workspace/FlameSpeed/References"

class ReferenceManager(models.Manager):
    def clean(self,List):
        return([x.strip() for x in List])# #I added this
    
    def populate_reference(self):
        RefFile = open(RefFile_PATH, 'r')
        for line in RefFile:
            data = self.clean(line.strip(' \n').split("\t"))
            reference = Reference(id_ref=data[0], source=data[1], title=data[2], authors=data[3], published_year=data[4])
            reference.save()        
        RefFile.close() 

class Reference(models.Model):
    objects = ReferenceManager()
    id_ref = models.IntegerField()
    source = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300)
    published_year = models.CharField(max_length=4)

class MixtureManager(models.Manager):
    def name_file(self,inFile_PATH):           
            data = os.path.basename(inFile_PATH).rstrip('\n\r').split(",")
            return data[0]
    
    def populate_mixture_characteristic(self):
        list_folders = os.listdir(PROJECT_PATH)
        for name_folder in list_folders:
            folderPath = glob.glob(PROJECT_PATH + name_folder) 
            list_files= os.listdir(folderPath[0])
            for name_file in list_files:
                reference_object = Reference.objects.get(id_ref = name_folder)
                inFile_PATH = folderPath[0]+'/'+name_file
                mixture = Mixture(name = self.name_file(inFile_PATH))
                mixture.save()
                mixture.references.add(reference_object)
                inFile = open(inFile_PATH, 'r')
                headtitle = inFile.readline().rstrip('\n\r').split(",")
                
                for line in inFile:
                    data = line.rstrip('\n\r').split("  ")
                    characteristic = Characteristic(name = headtitle[0], value=data[0], speed=data[1], pressure=headtitle[1], temperature=headtitle[2], nH2_nO2=headtitle[3], nN2_nO2=headtitle[4], CO=headtitle[5], CO2=headtitle[6], H2O=headtitle[7], N2=headtitle[8], details=headtitle[9], mixture = mixture, reference = reference_object)
                    characteristic.save()
      
class Mixture(models.Model):
    objects = MixtureManager()
    name = models.CharField(max_length=20, primary_key = True)
    references = models.ManyToManyField(Reference)
    
class Characteristic(models.Model):
    name = models.CharField(max_length=50)
    value = models.FloatField()
    speed = models.FloatField()
    pressure = models.CharField(max_length=200)
    temperature = models.CharField(max_length=200)
    nH2_nO2 = models.CharField(max_length=200)
    nN2_nO2 = models.CharField(max_length=200)
    CO = models.CharField(max_length=200)
    CO2 = models.CharField(max_length=200)    
    H2O = models.CharField(max_length=200) 
    N2 = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    mixture = models.ForeignKey(Mixture)
    reference = models.ForeignKey(Reference)
    