#Author-Derrik Adams
#Description-ME 578 Lab 1: Lab 1

import adsk.core, adsk.fusion, adsk.cam, traceback

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
        x2 = rad1
        y2 = 0
        z2 = 0
        rad2 = .156
        #Create circle at origin with radius of 2
        circle1 = circles1.addByCenterRadius(adsk.core.Point3D.create(x1,y1,z1), rad1)
        circle2 = circles2.addByCenterRadius(adsk.core.Point3D.create(x2,y2,z2), rad2)
                
        
        #ui.messageBox('ME 578 Lab 1: Lab 1')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
