#Author-Derrik Adams
#Description-ME 578 Lab 1: Lab 2

import adsk.core, adsk.fusion, adsk.cam, traceback, math

def run(context):
    ui = None
    try:
        #Doc setup
        app = adsk.core.Application.get()
        design = app.activeProduct
        rootComp = design.rootComponent
        ui  = app.userInterface
              
        #Create sketch on the xy plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        
        #Create 2 different sketches
        sketch1 = sketches.add(xyPlane)
        sketch2 = sketches.add(xyPlane)

        circles1 = sketch1.sketchCurves.sketchCircles
        circles2 = sketch2.sketchCurves.sketchCircles
        
        #Define first circle with center at origin and radius 2cm
        x1 = 0
        y1 = 0
        z1 = 0
        rad1 = 2
        
        #Define second circle with center on edge of first circle and radius .156cm
        x2 = 10
        y2 = 0
        z2 = 0
        rad2 = 1
        #Create circle at origin with radius of 2
        circle1 = circles1.addByCenterRadius(adsk.core.Point3D.create(x1,y1,z1), rad1)
        circle2 = circles2.addByCenterRadius(adsk.core.Point3D.create(x2,y2,z2), rad2)
                
        #Get the profile of each sketch
        circle1profile = sketch1.profiles.item(0)
        circle2profile = sketch2.profiles.item(0)
        
        #Get the Extrudes Collection
        extrudes = rootComp.features.extrudeFeatures
        
        #Create the input object for the extrusion of the first circle
        extrudeCircle1input = extrudes.createInput(circle1profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircle1distance = adsk.core.ValueInput.createByReal(4)
        extrudeCircle1input.setDistanceExtent(False, extrudeCircle1distance)
        
        
        #Create the input object for the extrusion of the second circle
        extrudeCircle2input = extrudes.createInput(circle2profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircle2distance = adsk.core.ValueInput.createByReal(4)        
        extrudeCircle2input.setDistanceExtent(False, extrudeCircle2distance)

        #Extrude circles 1 and 2        
        extrudeCircle1 = extrudes.add(extrudeCircle1input)
        extrudeCircle2 = extrudes.add(extrudeCircle2input)
        
        
        ## Section for obtaining selected faces on cylinders
        ui.messageBox('Select two cylindrical faces')
        
        #Obtain First item selected by the user
        firstSelectedItem = ui.selectEntity("Select First Point","SketchPoints,Vertices,ConstructionPoints,CylindricalFaces")
        firstSelectedItemValue = firstSelectedItem.point
        
        #Obtain Second item selected by the user
        secondSelectedItem = ui.selectEntity("Select Second Point","SketchPoints,Vertices,ConstructionPoints,CylindricalFaces")
        secondSelectedItemValue = secondSelectedItem.point

        #Find the distance between the two selected points
        distanceBetweenPoints = firstSelectedItemValue.distanceTo(secondSelectedItemValue)
        
        #Calculate the necessary belt length based on the distance found
        beta = 2*math.acos((rad1-rad2)/(2*distanceBetweenPoints))
        BeltLength = 2*distanceBetweenPoints*math.sin(beta/2)+(math.pi/2)*(2*rad1+2*rad2)+(math.pi/180)*(90-.5*beta)*(2*rad1-2*rad2)

        #display the distance between the cylinders in correct units 
        unitsMgr = design.unitsManager
        displayBeltLength = unitsMgr.formatInternalValue(BeltLength,unitsMgr.defaultLengthUnits,True)
        ui.messageBox('The needed belt length is: ' + displayBeltLength)
       
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))