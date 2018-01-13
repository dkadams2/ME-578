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
        sketch3 = sketches.add(xyPlane)

        circles1 = sketch1.sketchCurves.sketchCircles
        circles2 = sketch2.sketchCurves.sketchCircles
        circles3 = sketch3.sketchCurves.sketchCircles
        
        
        #Define first circle with center at origin and radius given by number of teeth desired
        numTeeth = 20
        teethSpacing = .5 #cm
        
        x1 = 0
        y1 = 0
        z1 = 0
        rad1 = numTeeth*teethSpacing/(2*math.pi)
        
        #Define second circle with center on edge of first circle and radius .156cm
        x2 = rad1
        y2 = 0
        z2 = 0
        rad2 = .156
        
        #Define third circle to cut out center of the gear
        x3 = 0
        y3 = 0
        z3 = 0
        rad3 = .5 #cm
        
        #Define the fourth circle to create the flange
        x4 = 0
        y4 = 0
        z4 = 0
        rad4 = 1.1*rad1
        
        #Create circle at origin with radius of 2
        circle1 = circles1.addByCenterRadius(adsk.core.Point3D.create(x1,y1,z1), rad1)
        circle2 = circles2.addByCenterRadius(adsk.core.Point3D.create(x2,y2,z2), rad2)
        circle3 = circles2.addByCenterRadius(adsk.core.Point3D.create(x3,y3,z3), rad3)
        circle4 = circles3.addByCenterRadius(adsk.core.Point3D.create(x4,y4,z4), rad4)
                
        #Get the profile of each sketch
        circle1profile = sketch1.profiles.item(0)
        circle2profile = sketch2.profiles.item(0)
        circle3profile = sketch2.profiles.item(1)
        circle4profile = sketch3.profiles.item(0)
        
        #Get the Extrudes Collection
        extrudes = rootComp.features.extrudeFeatures
        
        #Create the input object for the extrusion of the first circle
        extrudeCircle1input = extrudes.createInput(circle1profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircle1distance = adsk.core.ValueInput.createByReal(1.5)
        extrudeCircle1input.setDistanceExtent(False, extrudeCircle1distance)
        
        
        #Create the input object for the extrusion of the second circle
        extrudeCircle2input = extrudes.createInput(circle2profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeCircle2distance = adsk.core.ValueInput.createByReal(1.5)        
        extrudeCircle2input.setDistanceExtent(False, extrudeCircle2distance)
        
        #Create the input object for the extrusion of the third circle
        extrudeCircle3input = extrudes.createInput(circle3profile, adsk.fusion.FeatureOperations.CutFeatureOperation)
        extrudeCircle3distance = adsk.core.ValueInput.createByReal(1.5)  
        extrudeCircle3input.setDistanceExtent(False, extrudeCircle3distance)
        
        #Create the input object for the extrusion of the fourth circle
        extrudeCircle4input = extrudes.createInput(circle4profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        extrudeCircle4distance = adsk.core.ValueInput.createByReal(-.2)
        extrudeCircle4input.setDistanceExtent(False, extrudeCircle4distance)

        #Extrude and cut the four circles      
        extrudeCircle1 = extrudes.add(extrudeCircle1input)
        extrudeCircle2 = extrudes.add(extrudeCircle2input)
        extrudeCircle3 = extrudes.add(extrudeCircle3input)
        extrudeCircle4 = extrudes.add(extrudeCircle4input)
        
        #Create the circular array of circles subtracted to create teeth
        circularPatterns = rootComp.features.circularPatternFeatures

        #Create the entity collection to pass into the circular array input
        inputEntitiesCollection = adsk.core.ObjectCollection.create()
        inputEntitiesCollection.add(extrudeCircle2)  
        inputAxis = rootComp.zConstructionAxis          
        #Create the circular pattern input
        circularPatternInput = circularPatterns.createInput(inputEntitiesCollection, inputAxis)
        circularPatternInput.quantity = adsk.core.ValueInput.createByReal(numTeeth)
        circularPatternInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        
        circularPattern = circularPatterns.add(circularPatternInput)
        
        
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