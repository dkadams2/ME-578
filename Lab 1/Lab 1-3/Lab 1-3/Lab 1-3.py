#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, os

#Define the number of teeth and shaft diameter of the pulley as variables
numTeeth = 15
shaftDiameter = .5 #cm

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        #Access the import manager and root component
        importManager = app.importManager
        rootComp = app.activeProduct.rootComponent
        
        #Get filename and path of the file to load
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'squaretoothpulley.f3d')  
        
        #Create the input options for and give them to the target
        importOptions = importManager.createFusionArchiveImportOptions(filename)
        importManager.importToTarget(importOptions, rootComp)
        
        #Get the occurance of the importated pulley
        pulleyOccurance = rootComp.occurrences.item(rootComp.occurrences.count-1)
        
        #Make the number of teeth and shaft diameter parameters to change
        parameters = pulleyOccurance.component.parentDesign.allParameters
        teethNumParam = parameters.itemByName('teethNum')
        shaftDiameterParam = parameters.itemByName('shaftDiameter')
        teethNumParam.expression = str(numTeeth)
        shaftDiameterParam.expression = str(shaftDiameter) + 'cm'
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
