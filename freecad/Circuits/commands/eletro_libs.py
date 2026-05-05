# Função para iniciar a bancada 
# Copyright Lucas Losinskas 
# year 2023


# import os
# wbPath = os.path.dirname(__file__)
# iconPath = os.path.join(wbPath, 'Resources/Icons')

# from PySide import QtGui, QtCore
# import FreeCADGui as Gui
# import FreeCAD as App
# from FreeCAD import Console as FCC 


# # Tipo dos objetos de referência 
# datumTypes = [
#     'PartDesign::CoordinateSystem', 
#     'PartDesign::Plane', 
#     'PartDesign::Line', 
#     'PartDesign::Point'
# ]
# partInfo = [
#     'PartID', 
#     'PartName', 
#     'PartDescription', 
#     'PartSupplier'
# ]
# containerTypes = ['App::Part', 'PartDesign::Body']

# VEC_0 = App.Vector(0,0,0)
# VEC_X = App.Vector(1,0,0)
# VEC_Y = App.Vector(0,1,0)
# VEC_Z = App.Vector(0,0,1)
# VEC_T = App.Vector(1,1,1)

# rotX10 = App.Placement(VEC_0, App.Rotation(VEC_X, 10))
# rotY10 = App.Placement(VEC_0, App.Rotation(VEC_Y, 10))
# rotZ10 = App.Placement(VEC_0, App.Rotation(VEC_Z, 10))

# rotX = App.Placement(VEC_0, App.Rotation(VEC_X, 90))
# rotY = App.Placement(VEC_0, App.Rotation(VEC_Y, 90))
# rotZ = App.Placement(VEC_0, App.Rotation(VEC_Z, 90))


# def findObjectLink(obj, doc = App.ActivatDocument):
#     for o in doc.Objects: 
#         if hasattr(o, 'LinkedObject'):
#             if o.LinkedObject == obj:
#                 return o 
#     return(None)

# def gerSelectionPath(docName, objName, subObjName):
#     val = []
#     if (docName is None) or (docName == ''):
#         docName = App.ActiveDocument.Name
#     val.append(docName)
#     if objName and (objName!=''):
#         val.append(objName)
#         if subObjName and (subObjName != ''):
#             for son in subObjName.split('.'):
#                 val.append(son)
#     return val


# def cloneObject(obj):
#     container = obj.getParentGeoGroup()
#     result = None
#     if obj.Document and container:
#         result =  obj.Document.addObject('App::Link', obj.Name)
#         result.LinkedObject = obj
#         result.Label = obj.Label
#         container.addObject(result)
#         result.recompute()
#         container.recompute()
#         result.Document.recompute()
#     return result 


# def placeObjectToLCS(attObj, attLink, attDoc, attLCS):
#     expr = makeExpressionDatum( attLink, attDoc, attLCS)
#     if not hasattr(attObj, 'SolverId'):
#         makeAsmProperties(attObj)
#     attObj.AttachedBy = 'Origin'
#     attObj.AttachedTo = attLink+ '#' + attLCS
#     attObj.setExpression('Placement', expr)
#     attObj.SolverID = 'Asm4EE'
#     attObj.recompute()
#     container = attObj.getParentGeoFeatureGroup()
#     if container:
#         container.recompute()
#     if attObj.Document:
#         attObj.Document.recompute()
        