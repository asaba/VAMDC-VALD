# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from decimal import *
import commonfunctions as cf
import re

import dictionaries

from vamdctap.bibtextools import *
from vamdctap.generators import makeSourceRefs
import os
if os.getenv('ENV_USER_TZ', None):
    TIME_ZONE = os.getenv('ENV_USER_TZ') # changed to UTC

class ZeroPointMolecularStateClass():
    #object used for dissociation limit of ElectronicStates 
    def __init__(self, molecularspeciesID):
        #There are only one dissociation limit ElectronicStates for each MolecularSpecies
        #used the prefix Z to avoid collision with other ID  
        self.state_id = "Z" + str(molecularspeciesID)
        self.total_energy = 0
        self.description = "Dissociation limit"
        self.stateauxillary = 1

class GenericModelNotExpiredManager(models.Manager):
    def get_query_set(self):
        return self.get_alive_query_set()
    def get_alive_query_set(self, timecheck = None):
        wanted_items = set()
        for item in super(GenericModelNotExpiredManager, self).get_query_set().all():
            if not item.expired(timecheck):
                wanted_items.add(item.pk)
        return super(GenericModelNotExpiredManager, self).get_query_set().filter(pk__in = wanted_items)

class Author(object):
    def __init__(self, Name, Address):
        self.Name = Name
        self.Address = Address

class BibRef(object):
    # simple dummy object to define a Method 
    def __init__(self, SourceID, Category, SourceName, Year, Authors, Title):
        self.SourceID = SourceID
        self.Category = Category
        self.SourceName = SourceName
        self.Year = Year
        self.Authors = Authors
        self.Title = Title

class Method(object):
    # simple dummy object to define a Method 
    def __init__(self, mid, description, Sources):
        self.id = mid
        self.category = 'theory'
        self.description, tmpbib = description
        self.Sources = []
        for bib in tmpbib:
            if bib.bibtex:
                if not (bib in Sources):
                    self.Sources.append(bib)
        self.SourcesRef = [b.pk for b in self.Sources]
                    
        
class NormalMode(models.Model):
    def __init__(self, normalmode_id, frequency, intensity, sym_type, displacementvectors, electronicstate, elements, Methods, SourceRefs): 
        #electronicStateRef 
        self.pointgroupsymmetry = sym_type
        self.normalmodeidtype = normalmode_id #NormalModeIDType, defining unique identifier for this mode, to be referenced
        self.HarmonicFrequency = str(frequency * Decimal('29979.2458'))
        self.intensity = intensity
        self.electronicstate = electronicstate
        self.NormalModesMethod = Methods
        self.NormalModesSourceRef = SourceRefs
        if displacementvectors: 
            self.displacementvectors = eval(displacementvectors)
            self.displacementvectorsx = []
            self.displacementvectorsy = []
            self.displacementvectorsz = []
            self.displacementvectorselementref = []
            for index in range(len(elements)): #XXX
                self.displacementvectorselementref.append(elements[index])
                self.displacementvectorsx.append(self.displacementvectors[0 + index * 3 ])
                self.displacementvectorsy.append(self.displacementvectors[1 + index * 3 ])
                self.displacementvectorsz.append(self.displacementvectors[2 + index * 3 ])
        else:
            self.displacementvectors = None
    def returnXML(self, elements, method, RefSource, NodeName): 

        result = '<NormalMode id="V' + NodeName + "-" + str(self.normalmodeidtype) + '"'
        if self.pointgroupsymmetry:
            result += ' pointGroupSymmetry="' + self.pointgroupsymmetry + '"'
        if method:
            result += ' methodRef="M' + NodeName + "-" + str(method) + '"'
        result += '>\n'
        #result += returnXMLSource(RefSource, NodeName)
        result += '<HarmonicFrequency>\n'
        result += '<Value units="MHz">' + str(self.harmonicfrequency * Decimal('29979.2458')) + '</Value>\n'
        #result += '<Accuracy>1</Accuracy>\n'
        result += '</HarmonicFrequency>\n'
        result += '<Intensity>\n'
        result += '<Value units="km/mol">' + str(self.intensity) + '</Value>\n'
        result += '</Intensity>\n'
        if self.displacementvectors:
            result += '<DisplacementVectors units="1/cm">\n'
            for index in range(len(elements)): #XXX
                result += '<Vector ref="' + elements[index] + '"'
                result += ' x3="' + self.displacementvectors[0 + index * 3 ] + '"'
                result += ' y3="' + self.displacementvectors[1 + index * 3 ] + '"'
                result += ' z3="' + self.displacementvectors[2 + index * 3 ] + '"/>\n'
            result += '</DisplacementVectors>\n'
            
        result +="</NormalMode>\n"
        return result
        
class MolecularChemicalSpecies():
    def __init__(self, moleculestructure, MoleculeStructureMethod, MoleculeStructureSourceRef, normalmodes, NormalModesMethod, NormalModesSourceRef):
        #self.moleculestructure = moleculestructure.replace("<molecule>", '<cml xmlns="http://www.xml-cml.org/schema" xsi:schemaLocation="http://www.xml-cml.org/schema ../../schema.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">').replace("</molecule>", "</cml>")
        self.moleculestructure = moleculestructure
        self.MoleculeStructureMethod = MoleculeStructureMethod
        #self.normalmodes = returnXMLSource(NormalModesSourceRef, NodeName) + normalmodes
        #self.normalmodes = normalmodes
        #self.NormalModesMethod = NormalModesMethod
        #self.NormalModesSourceRef = NormalModesSourceRef
        self.MoleculeStructureSourceRef = MoleculeStructureSourceRef
        
    def CML(self):
        return self.moleculestructure.replace("<molecule>", "").replace("</molecule>", "").replace("atom ", "cml:atom ").replace("atomA", "cml:atomA").replace("bond", "cml:bond")


class Bibliography(models.Model):
    bib_id = models.AutoField(primary_key=True)
    type = models.ForeignKey('Reftype')
    series = models.ForeignKey('PublicationSeries')
    authors = models.ManyToManyField('Authors') # , through = "AuthorGroups"
    editors = models.ManyToManyField('Editors') # , through = "EditorsGroups"
    publisher = models.ForeignKey('Publishers')
    title = models.TextField(blank=True)
    volume = models.IntegerField(null=True, blank=True)
    doi = models.TextField(blank=True)
    page_begin = models.CharField(max_length = 45, blank=True)
    page_end = models.CharField(max_length = 45,blank=True)
    uri = models.TextField(blank=True)
    city = models.CharField(max_length = 45, blank=True)
    version = models.CharField(max_length = 45, blank=True)
    source_name = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    reference = models.TextField(blank=True)
    bibtex = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'bibliography'
    def authorlist(self):
        result = u""
        for a in self.authors.all():
            result += a.name + u"; "
        return result
    def __unicode__(self):
        return self.title + self.authorlist()
    def XML(self):
        """
        This function replace the source ID with the database ID Bibliography record
        and return the hard XML code by the function BibTeX2XML
        """
        try: NODEID = dictionaries.RETURNABLES['NodeID']
        except: NODEID = 'PleaseFillTheNodeID'
        if self.bibtex:
            r = r"sourceID=\"B"+ NODEID + r"-.*\""
            newidvalue = u'sourceID="B'+ NODEID + u"-" + str(self.bib_id) + u'"'
            result = re.sub(r, newidvalue,  BibTeX2XML( self.bibtex ))
            return unicode(result)
    def bibtextoref(self):
        if self.bibtex:
            from pybtex.database.input import bibtex
            parser = bibtex.Parser()
            bib_data = parser.parse_stream(self.bibtex)
            if "title" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_title = bib_data.entries[bib_data.entries.keys(0)].fields['title']
            else:
                tmp_title = None
            if "pages" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_page_begin, tmp_page_end  = re.split(r"[,-]", bib_data.entries[bib_data.entries.keys(0)].fields['pages'])
            if "volume" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_volume = bib_data.entries[bib_data.entries.keys(0)].fields['volume']
            if "doi" in bib_data.entries[bib_data.entries.keys(0)].fields:
                tmp_doi = bib_data.entries[bib_data.entries.keys(0)].fields['doi']
            return BibRef(self.bib_id, "book", "SourceName", "2011", [Author("Author01", None), Author("Author02", None)], tmp_title)

    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class Authors(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True, verbose_name = "e-mail")
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'authors'
    def __unicode__(self):
        return self.name
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()


class BasisSets(models.Model):
    basisset_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 45, blank=True, null=True,)
    description = models.TextField(blank=True, null=True,)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'basissets'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring


class BasisSetsBibliographies(models.Model):
    id = models.AutoField(primary_key=True)
    basissets = models.ForeignKey('BasisSets')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'basissets_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class BibliographyAuthors(models.Model):
    id = models.AutoField(primary_key=True)
    authors = models.ForeignKey('Authors')
    bibliographies = models.ForeignKey('Bibliography')
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'bibliography_authors'

class BibliographyEditors(models.Model):
    id = models.AutoField(primary_key=True)
    bibliographies = models.ForeignKey('Bibliography')
    editors = models.ForeignKey('Editors')
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'bibliography_editors'

class CalculationGroups(models.Model):
    calcgroup_id = models.AutoField(primary_key=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculationgroups'
        

class ChemistryCodes(models.Model):
    code_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, null = True, blank=True)
    version = models.CharField(max_length = 45, null = True, blank=True)
    description = models.TextField( null = True, blank=True)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(blank=True, null = True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'chemistrycodes'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        return self.name + " - " + self.version

class Calculations(models.Model):
    calc_id = models.AutoField(primary_key=True)
    code = models.ForeignKey('ChemistryCodes')
    input = models.TextField(blank=True) 
    input_md5 = models.CharField(max_length = 45, blank=True)
    output = models.TextField(blank=True)
    output_md5 = models.CharField(max_length = 45, blank=True)
    other_output = models.TextField(blank=True)
    other_output_md5 = models.CharField(max_length = 45, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculations'
                
    def __unicode__(self):
        stringreturn = ""
        if self.time_stamp:
            stringreturn += "Entry date: " + self.time_stamp + "\n"
        if self.qual_index:
            stringreturn += "Quality index: " + self.qual_index + "\n"
        if self.code:
            stringreturn += "code: " + str(self.code) + "\n"
        if self.input_md5:
            stringreturn += "Input File md5: " + self.input_md5 + "\n"
        if self.output_md5:
            stringreturn += "Output File md5: " + self.output_md5 + "\n"
        if self.other_output_md5:
            stringreturn += "Other Output File md5: " + self.other_output_md5 + "\n"
        if len(stringreturn) > 0:
            return stringreturn
        else:
            return "No Data"

class CalculationLists(models.Model):
    calc_list_id = models.AutoField(primary_key=True)
    calcgroup = models.ForeignKey('CalculationGroups')
    calc = models.ForeignKey('Calculations')
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'calculationlists'



class ChemistryCodesBibliographies(models.Model):
    id = models.AutoField(primary_key=True)
    chemistrycodes = models.ForeignKey('ChemistryCodes')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'chemistrycodes_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class DdResonances(models.Model):
    dd_id = models.AutoField(primary_key=True)
    vibanalisysanarmonic = models.ForeignKey('VibrationalAnalysesAnarmonic')
    vib_id1 = models.ForeignKey('TabulatedVibrations', db_column='vib_id1', related_name='vib_id1')
    vib_id2 = models.ForeignKey('TabulatedVibrations', db_column='vib_id2', related_name='vib_id2')
    k = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'ddresonances'

class DipoleMoments(models.Model):
    dip_id = models.AutoField(primary_key=True)
    state = models.ForeignKey('ElectronicStates')
    task = models.ForeignKey('Tasks')
    mu_x = models.FloatField()
    mu_y = models.FloatField()
    mu_z = models.FloatField()
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'dipolemoments'
    def __unicode__(self):
        return u"mu_x: " + str(self.mu_x) + u" mu_y: " + str(self.mu_y) + u" mu_z: " + str(self.mu_z)
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class DipoleMomentsBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    dipolemoments = models.ForeignKey('DipoleMoments')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'dipolemoments_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

#class DjangoAdminLog(models.Model):
#    id = models.IntegerField(primary_key=True)
#    action_time = models.DateTimeField()
#    user_id = models.IntegerField()
#    content_type_id = models.IntegerField(null=True, blank=True)
#    object_id = models.TextField(blank=True)
#    object_repr = models.CharField(max_length=600)
#    action_flag = models.IntegerField()
#    change_message = models.TextField()
#    class Meta:
#        db_table = u'django_admin_log'

#class DjangoContentType(models.Model):
#    id = models.IntegerField(primary_key=True)
#    name = models.CharField(max_length=300)
#    app_label = models.CharField(unique=True, max_length=255)
#    model = models.CharField(unique=True, max_length=255)
#    class Meta:
#        db_table = u'django_content_type'

#class DjangoSession(models.Model):
#    session_key = models.CharField(max_length=120, primary_key=True)
#    session_data = models.TextField()
#    expire_date = models.DateTimeField()
#    class Meta:
#        db_table = u'django_session'

#class DjangoSite(models.Model):
#    id = models.IntegerField(primary_key=True)
#    domain = models.CharField(max_length=300)
#    name = models.CharField(max_length=150)
#    class Meta:
#        db_table = u'django_site'

class Editors(models.Model):
    editor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 45, blank=True)
    address = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'editors'
    def __unicode__(self):
        return self.name
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() # The Dahl-specific manager.




class ElectronicStatesBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    electronicstates = models.ForeignKey('ElectronicStates')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'electronicstates_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class ElectronicTransitions(models.Model):
    transition_id = models.AutoField(primary_key=True)
    low_state = models.ForeignKey('ElectronicStates', related_name = 'low_state')
    up_state = models.ForeignKey('ElectronicStates', related_name = 'up_state')
    task = models.ForeignKey('Tasks')
    energy = models.FloatField(null=True, blank=True)
    osc_strenght = models.FloatField(null=True, blank=True)
    mu_x = models.FloatField(null=True, blank=True)
    mu_y = models.FloatField(null=True, blank=True)
    mu_z = models.FloatField(null=True, blank=True)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'electronictransitions'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class ElectronicTransitionsBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    electronictransitions = models.ForeignKey('ElectronicTransitions')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'electronictransitions_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()


class Elements(models.Model): 
    element_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    symbol = models.CharField(max_length = 45, blank=True)
    atomic_number = models.IntegerField(null=True, blank=True)
    atomic_mass = models.IntegerField(null=True, blank=True)
    element_group = models.CharField(max_length = 45, blank=True)
    standard_atomic_weight = models.FloatField(null=True, blank=True)
    isotope_of = models.ForeignKey("self", null=True, blank=True)
    class Meta:
        db_table = u'elements'
    def __unicode__(self):
        return self.name + "(" + self.symbol + ", " + str(self.atomic_number) +  ", " + str(self.atomic_mass) + ")"
    def electron_number(self):
        return self.atomic_number

class Xcclasses(models.Model):
    xcclasses_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'xcclasses'
    def __unicode__(self):
        if self.xcclasses_id:
            if self.name:
                return u"XC Class " + str(self.name)
            else:
                return u"XC Class " + str(self.xcclasses_id)
        else:
            return u"XC Class 0"
        
class Geometryclasses(models.Model):
    geometryclass_id = models.AutoField(primary_key=True)
    geometry = models.TextField(blank=True, verbose_name = "Geometry (CML Format)")
    geometry_md5 = models.CharField(max_length = 45, blank=True)
    sym_group = models.TextField(blank=True, verbose_name = "Symmetry Group")
    sym_elements = models.TextField(blank=True, verbose_name = "Symmetry Elements")
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'geometryclasses'
    def __unicode__(self):
        if self.geometryclass_id:
            return u"Geometry Class " + str(self.geometryclass_id)
        else:
            return u"Geometry Class 0"
    def calculate_md5(self):
        if self.geometry:
            self.geometry_md5 = returnmd5(re.split("[\r\n]+", unicode(self.geometry), 2)[2])  
    def returncmlstructure(self):
        #this function return the geometry stored in self.geometry (cml format)
        return self.geometry 

class FermiResonances(models.Model):
    fermi_id = models.AutoField(primary_key=True)
    vibanalisysanarmonic = models.ForeignKey('VibrationalAnalysesAnarmonic')
    vib_id1 = models.ForeignKey('TabulatedVibrations', db_column='vib_id1', related_name='vib_id3')
    vib_id2 = models.ForeignKey('TabulatedVibrations', db_column='vib_id2', related_name='vib_id4')
    vib_id3 = models.ForeignKey('TabulatedVibrations', db_column='vib_id3', related_name='vib_id5')
    fi = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'fermiresonances'

class Geometries(models.Model):
    geom_id = models.AutoField(primary_key=True)
    geometry = models.TextField(blank=True, verbose_name = "Geometry (CML Format)")
    geometry_md5 = models.CharField(max_length = 45, blank=True)
    sym_group = models.TextField(blank=True, verbose_name = "Symmetry Group")
    sym_elements = models.TextField(blank=True, verbose_name = "Symmetry Elements")
    geometryclass = models.ForeignKey('Geometryclasses')
    geometryclass_rotationalmatrix = models.TextField(blank=True, verbose_name = "Rotational Matrix")
    geometryclass_errors = models.TextField(blank=True, verbose_name = "Geometry Error")
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'geometries'
    def __unicode__(self):
        result = u""
        electronicstates = ElectronicStates.alive_objects.filter(geom = self.geom_id, is_minimum = True )
        if len(electronicstates) > 0:
            if self.geometry_md5:
                result += u"MD5: " + self.geometry_md5 + u", "
            if self.sym_group:
                result += u"Symmetry Group:" + self.sym_group + u", "
            result += unicode(electronicstates[0].species)
            
        else:
            if self.geometry_md5:
                result =  u"MD5: " + self.geometry_md5
            else:
                result =  self.geometry[0:20] + u"..."
        return result
            
    def calculate_md5(self):
        if self.geometry:
            self.geometry_md5 = returnmd5(re.split("[\r\n]+", unicode(self.geometry), 2)[2])  
    def returncmlstructure(self, SourceRefIDs = None):
        #this function return the geometry stored in self.geometry (cml format)
        if SourceRefIDs:
            return makeSourceRefs(SourceRefIDs) + self.geometry 
        else:
            return self.geometry 
    def returnelementslist(self):
        #this function return the list of elements
        result = []
        atoms = re.findall('id=".*" element', self.geometry)
        for row in atoms:
            s = row.split('"')
            result.append(s[1])
            #result.append(s[3] + s[1].replace("a", None))
        return result
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()


class IonisationEnergies(models.Model):
    ion_id = models.AutoField(primary_key=True)
    start_state = models.ForeignKey('ElectronicStates', related_name = 'start_state')
    ion_state = models.ForeignKey('ElectronicStates', related_name = 'ion_state')
    iontype = models.ForeignKey('IonisationTypes')
    energy = models.FloatField(null=True, blank=True)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'ionisationenergies'
    def __unicode__(self):
        result = u""
        if self.start_state.species.inchi:
            result += u"from " + self.start_state.species.inchi
        if self.ion_state.species.inchi:
            result += u" to " + self.ion_state.species.inchi
        if self.iontype:
            result += u", Type " + self.iontype.description
        if self.energy:
            result += u", Energy " + str(self.energy)
        return result
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class IonisationEnergiesBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    ionisationenergies = models.ForeignKey('IonisationEnergies')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'ionisationenergies_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 
    
class IonisationTypes(models.Model):
    iontype_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'ionisationtypes'
    def __unicode__(self):
        result = u""
        if self.description:
            result = u"IonType: " + self.description
        else:
            if self.iontype_id:
                result =  u"IonType ID: " + str(self.iontype_id)
            else:
                result =  u"IonType ID: 0"
        return result
        
class MolecularSpecies(models.Model):
    species_id = models.AutoField(primary_key=True)
    name = models.TextField(null=True, blank=True)
    formula = models.TextField(null=True, blank=True, verbose_name = "Stoichiometryc Formula")
    inchi = models.TextField(null=True, blank=True)
    inchikey = models.CharField(max_length = 45, blank=True)
    aromatic_cycles = models.IntegerField(null=True, blank=True)
    charge = models.IntegerField(null=True, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    isotopologue_of = models.ForeignKey("self", blank=True, null=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    
    def _get_molweight(self): return self.molweight()
    def _set_molweight(self, value): pass
    totalmolweight = property(_get_molweight,_set_molweight)
    
    class Meta:
        db_table = u'molecularspecies'
    def __unicode__(self):
        return_string = u""
        if self.name:
            return_string += u"name: " + self.name + u"; "
        if self.formula:
            return_string += u"formula: " + self.formula + u"; "
        if self.charge:
            return_string += u"charge: " + str(self.charge) + u"; "
        if len(return_string)>0:
            return_string = return_string[:-2]
        else:
            return_string = u"Inchi: " + self.inchi
        return return_string
    def atoms(self):
        result = []
        for element in self.elementspecies_set.all():
            result.append(element)
        return result
    def electrons_number(self):
        electrons = 0
        for tmp_atom in self.atoms():
            electrons += tmp_atom.electron_number()
        electrons += self.charge
        return electrons
    def inchi_without_charge(self):
        if self.inchi:
            return self.inchi.split("/q")[0].strip()
        else:
            #Error
            return "Inchi undefined"
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    def molweight(self):
        weight = 0
        if self.species_id:
            elements_species = ElementSpecies.objects.filter(species = self)
            for e in elements_species:
                weight += e.element.standard_atomic_weight
        return weight
    def OrdinaryStructuralFormula(self):
        result = u""
        if self.formula:
            s = False
            for c in self.formula:
                if re.match(r"[0-9]", c):
                    if not s:
                        result += u"\u005F{" + c
                        s = True
                    else:
                        result += c
                else:
                    if s:
                        result += u"}" + c
                        s = False
                    else:
                        result += c
            if s:
                result += u"}"
            result = u"$" + result  + u"$" 
        else:
            result += u"$NOFORMULA$"
        return result
    
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()
        
class ElementSpecies(models.Model):
    elemspecies_id = models.AutoField(primary_key=True)
    element = models.ForeignKey('Elements')
    species = models.ForeignKey('MolecularSpecies')
    number = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'elementspecies'

class Polarisabilities(models.Model):
    pol_id = models.AutoField(primary_key=True)
    state = models.ForeignKey('ElectronicStates')
    task = models.ForeignKey('Tasks')
    bibliographies = models.ManyToManyField('Bibliography')
    low_freq_lim = models.FloatField(null=True, blank=True)
    up_freq_lim = models.FloatField(null=True, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'polarisabilities'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class PolarisabilitiesBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    polarisabilities = models.ForeignKey('Polarisabilities')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'polarisabilities_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class PublicationSeries(models.Model):
    series_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    shortname = models.TextField(max_length = 200, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'publicationseries'

class Publishers(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 200, blank=True)
    address = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'publishers'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class Reftype(models.Model):
    type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length = 200,blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'reftype'
    def __unicode__(self):
        if self.description:
            return self.description
        else:
            return u"NO DESCRIPTION"
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 




class RotationalConstantsBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    rotationalcostants = models.ForeignKey('RotationalConstants')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'rotationalconstants_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class TabulatedChis(models.Model):
    chiid = models.AutoField(primary_key=True)
    vibanalisysanarmonic = models.ForeignKey('VibrationalAnalysesAnarmonic')
    vib_id1 = models.ForeignKey('TabulatedVibrations', db_column='vib_id1', related_name='vib_id6')
    vib_id2 = models.ForeignKey('TabulatedVibrations', db_column='vib_id2', related_name='vib_id7')
    chi = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'tabulatedchis'

class TabulatedPolarisabilities(models.Model):
    poltable_id = models.AutoField(primary_key=True)
    pol = models.ForeignKey('Polarisabilities')
    frequency = models.FloatField()
    re_alpha_xx = models.FloatField(null=True, blank=True)
    im_alpha_xx = models.FloatField(null=True, blank=True)
    re_alpha_yy = models.FloatField(null=True, blank=True)
    im_alpha_yy = models.FloatField(null=True, blank=True)
    re_alpha_zz = models.FloatField(null=True, blank=True)
    im_alpha_zz = models.FloatField(null=True, blank=True)
    re_alpha_xy = models.FloatField(null=True, blank=True)
    im_alpha_xy = models.FloatField(null=True, blank=True)
    re_alpha_xz = models.FloatField(null=True, blank=True)
    im_alpha_xz = models.FloatField(null=True, blank=True)
    re_alpha_yz = models.FloatField(null=True, blank=True)
    im_alpha_yz = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = u'tabulated_polarisabilities'


        
class TheoryLevels(models.Model):
    thlevel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 45, blank=True)
    description = models.TextField(blank=True)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    xc_name = models.TextField(blank=True)
    xc_description = models.TextField(blank=True)
    comments = models.TextField(blank=True, null=True)
    class Meta:
        db_table = u'theorylevels'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring

    #def fullprint(self):
    #    print "th_level_id:" + str(self.th_level_id) + "name:" + str(self.name) + "description:" + str(self.description) + "time_stamp:" + str(self.time_stamp) + "qual_index:"  + str(self.qual_index) + "comments:" + str(self.comments)

class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    thlevel = models.ForeignKey('TheoryLevels')
    calc = models.ForeignKey('Calculations')
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    class Meta:
        db_table = u'tasks'
    def __unicode__(self):
        returnstring = ""
        if self.name:
            returnstring += self.name
        else:
            returnstring += "NO NAME"
        if self.description:
            returnstring += " - " + self.description
        return returnstring
    def usedbasissets(self):
        bs_list_id = []
        for bs in self.elementspeciesbasisset_set.all():
            if bs.basisset in bs_list_id:
                pass
            else:
                bs_list_id.append(bs.basisset)
        return bs_list_id
    def returnmethoddescriptionandbib(self):
        methoddescription = ""
        bibliographies = []
        #Chemistry code
        methoddescription += "implementation: " + self.calc.code.name + " " + self.calc.code.version + "\n"
        for bib in self.calc.code.bibliographies.all():
            if not (bib in bibliographies):
                bibliographies.append(bib)
        #Theory level
        methoddescription += "theory: " + self.thlevel.description + "\n"
        if self.thlevel.xc_name:
            methoddescription += "xc: " + self.thlevel.xc_description + "\n"
        for bib in self.thlevel.bibliographies.all():
            if not (bib in bibliographies):
                bibliographies.append(bib)
        #Basis sets
        bslist = self.usedbasissets()
        if len(bslist) > 0:
            methoddescription += "basis sets: "
            for bs in bslist:
                methoddescription += bs.name + ", "
                for bib in bs.bibliographies.all():
                    if not (bib in bibliographies):
                        bibliographies.append(bib)
            methoddescription = methoddescription[:-2] + "\n"
        return methoddescription, bibliographies
    
class ElectronicStates(models.Model):
    state_id = models.AutoField(primary_key=True)
    species = models.ForeignKey('MolecularSpecies')
    geom = models.ForeignKey('Geometries')
    task = models.ForeignKey('Tasks')
    bibliographies = models.ManyToManyField('Bibliography')
    total_energy = models.FloatField(null=True, blank=True)
    is_minimum = models.BooleanField(null=False)
    rel_energy = models.FloatField(null=True, blank=True)
    electronicstateenergy = models.ForeignKey("self", null=True, blank=True)
    symmetry = models.TextField(blank=True)
    multiplicity = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True)
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'electronicstates'
    def __unicode__(self):
        returnstring = ""
        if self.total_energy:
            returnstring += "Total Energy: " + str(self.total_energy) + "; "
        if self.multiplicity:
            returnstring += "Multiplicity: " + str(self.multiplicity)
        return returnstring
    def countatoms(self):
        return self.species.atoms.count()
    def return_basissets_for_atoms(self):
        #return a list of tuple (atom, basisset)
        result = []
        esset = self.task.elementspeciesbasisset_set.all()
        for es_bs in esset.order_by('elementspecies__element').order_by('basisset'):
            result.append(es_bs)
        return result
    def equal_basis_set(self, basissets_for_atoms):
        mybasissets_for_atoms = self.return_basissets_for_atoms()
        result = True
        if len(mybasissets_for_atoms) == len(basissets_for_atoms):
            for i in range(len(mybasissets_for_atoms)):
                if mybasissets_for_atoms[i].elementspecies.element != basissets_for_atoms[i].elementspecies.element or mybasissets_for_atoms[i].basisset != basissets_for_atoms[i].basisset:
                    result = False
                    break
        else:
            return False
        return result
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()
    
class RotationalConstants(models.Model):
    rot_id = models.AutoField(primary_key=True)
    state = models.ForeignKey('ElectronicStates')
    a = models.FloatField(null=True, blank=True)
    b = models.FloatField(null=True, blank=True)
    c = models.FloatField(null=True, blank=True)
    wilson_dj = models.FloatField(null=True, blank=True)
    wilson_djk = models.FloatField(null=True, blank=True)
    wilson_dk = models.FloatField(null=True, blank=True)
    nielsen_dj = models.FloatField(null=True, blank=True)
    nielsen_djk = models.FloatField(null=True, blank=True)
    nielsen_dk = models.FloatField(null=True, blank=True)
    nielsen_d_j = models.FloatField(null=True, blank=True)
    nielsen_r5 = models.FloatField(null=True, blank=True)
    nielsen_r6 = models.FloatField(null=True, blank=True)
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'rotationalconstants'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class TheoryLevelsBibliographies(models.Model):
    id = models.AutoField(primary_key=True)
    theorylevels = models.ForeignKey('TheoryLevels')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'theorylevels_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class VanDerWaals(models.Model):
    vanderwaals_id = models.AutoField(primary_key=True)
    state_id_1 = models.ForeignKey('ElectronicStates', db_column='state_id_1', related_name='state_id_1')
    state_id_2 = models.ForeignKey('ElectronicStates', db_column='state_id_2', related_name='state_id_2')
    task = models.ForeignKey('Tasks')
    bibliographies = models.ManyToManyField('Bibliography')
    effective_freq = models.FloatField(null=True, blank=True)
    c6 = models.FloatField(null=True, blank=True)
    k = models.FloatField(null=True, blank=True)
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vanderwaals'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class VanDerWallsBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    vanderwalls = models.ForeignKey('VanDerWaals')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vanderwalls_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager() 

class VibrationalAnalysesAnarmonic(models.Model):
    vibanalysesanarmonic_id = models.AutoField(primary_key=True)
    polymode = models.TextField(blank=True)
    state = models.ForeignKey('ElectronicStates')
    task = models.ForeignKey('Tasks')
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vibrationalanalysesanarmonic'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()
           
class Vibrationalanalysesharmonic(models.Model):
    vibrationalanalysesharmonic_id = models.AutoField(primary_key=True)
    state = models.ForeignKey('Electronicstates')
    task = models.ForeignKey('Tasks')
    bibliographies = models.ManyToManyField('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vibrationalanalysesharmonic'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()


            


class TabulatedVibrations(models.Model):
    vib_id = models.AutoField(primary_key=True) #Probably problem whit bigint
    vibrationalanalysesharmonic = models.ForeignKey('Vibrationalanalysesharmonic')
    sym_type = models.TextField(blank=True)
    frequency = models.FloatField(null=True, blank=True)
    ir_intensity = models.FloatField(null=True, blank=True)
    alpha_a = models.FloatField(null=True, blank=True)
    alpha_b = models.FloatField(null=True, blank=True)
    alpha_c = models.FloatField(null=True, blank=True)
    diff_mu_x = models.FloatField(null=True, blank=True)
    diff_mu_y = models.FloatField(null=True, blank=True)
    diff_mu_z = models.FloatField(null=True, blank=True)
    eigenvectors = models.TextField(blank=True)
    class Meta:
        db_table = u'tabulatedvibrations'
    def __unicode__(self):
        return_string = ""
        if self.sym_type:
            return_string += "sym_type: " + str(self.sym_type) + "; "
        if self.frequency:
            return_string += "frequency: " + str(self.frequency) + "; "
        if self.alpha_a:
            return_string += "alpha_a: " + str(self.alpha_a) + "; "
            return_string += "alpha_b: " + str(self.alpha_b) + "; "
            return_string += "alpha_c: " + str(self.alpha_c) + "; "
        if self.diff_mu_x:
            return_string += "diff_mu_x: " + str(self.diff_mu_x) + "; "
            return_string += "diff_mu_y: " + str(self.diff_mu_y) + "; "
            return_string += "diff_mu_z: " + str(self.diff_mu_z) + "; "
        if return_string:
            return return_string[:-2]
        else:
            return "Empty"


class VibrationalanalysesharmonicBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    vibrationalanalysesharmonic = models.ForeignKey('Vibrationalanalysesharmonic')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vibrationalanalysesharmonic_bibliographies' 
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

        
class VibrationalAnalysesAnarmonicBibliographies(models.Model):
    id = models.AutoField(primary_key= True)
    vibrationalanalysisanarmonic = models.ForeignKey('VibrationalAnalysesAnarmonic')
    bibliography = models.ForeignKey('Bibliography')
    time_stamp = models.DateTimeField(null=True, blank=True)
    qual_index = models.IntegerField(null=True, blank=True, verbose_name = "Quality Index")
    comments = models.TextField(blank=True)
    time_exp = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'vibrationalanalysesanarmonic_bibliographies'
    def now(self, force=False):
        if force or not self.time_stamp:
            self.time_stamp = cf.datatimenow()
    def expire(self):
        return cf.dataexpire(self)
    def expired(self, timecheck = None):
        return cf.checkexpired(self, timecheck)
    expired.boolean = True
    objects = models.Manager() # The default manager.
    alive_objects = GenericModelNotExpiredManager()

class ElementSpeciesBasisSet(models.Model):
    elementspecies_basisset_id = models.AutoField(primary_key= True)
    basisset = models.ForeignKey('BasisSets')
    task = models.ForeignKey('Tasks')
    elementspecies = models.ForeignKey('ElementSpecies')
    
    class Meta:
        db_table = u'elementspecies_basisset'
