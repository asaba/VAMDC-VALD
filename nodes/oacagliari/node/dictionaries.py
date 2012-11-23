RETURNABLES = {
'NodeID':'OACagliari',
'MethodID':'Method.id',
'MethodCategory':'Method.category',
'MethodSourceRef':'Method.SourcesRef',
'MethodDescription':'Method.description',

#'AtomMass':'Atom.standard_atomic_weight',
#'AtomMassNumber':'Atom.atomic_mass',
#'AtomSymbol':'Atom.symbol',
#'MethodDescription': 'Method.category',
'MoleculeChemicalName':'Molecule.name',
'MoleculeInchi':'Molecule.inchi',
'MoleculeInchiKey':'Molecule.inchikey',
'MoleculeIonCharge':'Molecule.charge',
'MoleculeComment': 'Molecule.comments',
'MoleculeMolecularWeight':'Molecule.molweight()',
'MoleculeMolecularWeightUnit': u"amu",
#'MoleculeQnCase':'MoleQNs.',
'MoleculeSpeciesID':'Molecule.pk',
"MoleculeStateEnergyOrigin": 'MoleculeState.StateEnergyOrigin', #"assuming zero at infinity",
'MoleculeStateEnergy':'MoleculeState.total_energy',
'MoleculeStateEnergyMethod':'MoleculeState.energymethod', #kkk
'MoleculeStateEnergyRef' : 'MoleculeState.StateEnergySourceRef', #kkk electronic state
'MoleculeStateAuxillary' : 'MoleculeState.stateauxillary',

'MoleculeStateEnergyUnit':u'au', #TO CHANGE
'MoleculeStateDescription': 'MoleculeState.description',
'MoleculeStateID':'MoleculeState.state_id',
'MoleculeOrdinaryStructuralFormula':'Molecule.OrdinaryStructuralFormula()',
'MoleculeStoichiometricFormula':'Molecule.formula',
'MoleculeStructure': "Molecule.molecularchemicalspecies",
'MoleculeStructureMethod': "MoleculeStructure.MoleculeStructureMethod", #kkk
'MoleculeStructureSourceRef': "MoleculeStructure.MoleculeStructureSourceRef", #kkk electronic state

#Normal Modes
'MoleculeNormalModes': 'Molecule.NomalModes', #'Molecule.',
'MoleculeNormalModesMethod' : 'NormalMode.NormalModesMethod',
'MoleculeNormalModesRef' : 'NormalMode.NormalModesSourceRef', #vibration analysis
'MoleculeNormalModeElectronicState': 'NormalMode.electronicstate', #'Molecule.',
'MoleculeNormalModePointGroupSymmetry': 'NormalMode.pointgroupsymmetry', #'Molecule.',
'MoleculeNormalModeID' : 'NormalMode.normalmodeidtype',
'MoleculeNormalModeHarmonicFrequency' : 'NormalMode.HarmonicFrequency',#[0].HarmonicFrequency
'MoleculeNormalModeHarmonicFrequencyUnit' : u"MHz",
'MoleculeNormalModeIntensity' : 'NormalMode.intensity',
'MoleculeNormalModeIntensityUnit' : u"km/mol", 
'MoleculeNormalModeDisplacementVectorX3' : 'NormalMode.displacementvectorsx',
'MoleculeNormalModeDisplacementVectorY3' : 'NormalMode.displacementvectorsy',
'MoleculeNormalModeDisplacementVectorZ3' : 'NormalMode.displacementvectorsz',
'MoleculeNormalModeDisplacementVectorRef' : 'NormalMode.displacementvectorselementref',
'MoleculeNormalModeDisplacementVectorsUnit' : '1/cm',

#'Sources' : 'Source' ,
#'SourceAuthors':'Source.Authors',
#'SourceCategory':'Source.category',
'SourceID':'Source.bib_id',
'SourceAuthorName':'Source.author',
'SourceCategory':'Source.category',
'SourcePageBegin':'Source.pages',
'SourcePageEnd':'Source.pages',
'SourceName':'Source.journal',
'SourceTitle':'Source.title',
'SourceURI':'Source.url',
'SourceVolume':'Source.volume',
'SourceYear':'Source.year',

}



RESTRICTABLES = { 
'AsOfDate':'time_stamp',
#'AtomMass':'elementspecies__element__standard_atomic_weight',
#'AtomMassNumber':'elementspecies__element__atomic_mass',
#'AtomSymbol':'elementspecies__element__symbol',
'MoleculeChemicalName':'name',
'Inchi':'inchi',
'InchiKey':'inchikey',
'IonCharge':'charge',
'MoleculeStateEnergy':'electronicstates__total_energy',
'MoleculeStateID':'electronicstates__state_id',
'MoleculeStoichiometricFormula':'formula',
#'MoleculeMolecularWeight':'totalmolweight',
'MoleculeNormalModeHarmonicFrequency' : 'electronicstates__vibrationalanalysesharmonic__tabulatedvibrations__frequency',
'MoleculeNormalModeIntensity' : 'electronicstates__vibrationalanalysesharmonic__tabulatedvibrations__ir_intensity',
}



# Do not edit or remove these three lines
#from vamdctap.caselessdict import CaselessDict
#RETURNABLES = CaselessDict(RETURNABLES)
#RESTRICTABLES = CaselessDict(RESTRICTABLES)

