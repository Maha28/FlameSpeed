from django.db import models
import glob, os, pdb
PROJECT_PATH = "/home/maha/workspace/FlameSpeed/Data/"
RefFile_PATH = "/home/maha/workspace/FlameSpeed/References"

class ReferenceManager(models.Manager):
    def clean(self,List):
        return([x.strip() for x in List])
    
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
                headtitle = inFile.readline().rstrip('\n\r').split("  ")
                characteristic_name = headtitle[0]
                characteristic_press_temp = headtitle[1]
                characteristic_conditions = headtitle[2]
                for line in inFile:
                    data = line.rstrip('\n\r').split("  ")
                    characteristic = Characteristic(name = characteristic_name,value=data[0], speed=data[1], press_temp=characteristic_press_temp, conditions=characteristic_conditions, mixture = mixture, reference = reference_object)
                    characteristic.save()
      
class Mixture(models.Model):
    objects = MixtureManager()
    name = models.CharField(max_length=20, primary_key = True)
    references = models.ManyToManyField(Reference)
    
class Characteristic(models.Model):
    name = models.CharField(max_length=50)
    value = models.FloatField()
    speed = models.FloatField()
    press_temp = models.CharField(max_length=300)
    conditions = models.CharField(max_length=300)
    mixture = models.ForeignKey(Mixture)
    reference = models.ForeignKey(Reference)
    