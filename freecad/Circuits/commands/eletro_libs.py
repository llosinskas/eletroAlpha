"""
Biblioteca de funções utilitárias para a bancada Circuits.
Fornece helpers para criação de objetos, grupos e manipulação de geometria.
"""

import FreeCAD as App
import FreeCADGui as Gui
import os

# Paths base
wbPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
iconPath = os.path.join(wbPath, 'Resources', 'Icons')


def create_group(name, doc=None):
    """
    Cria um grupo (App::DocumentObjectGroup) no documento se ele não existir.
    
    Args:
        name (str): Nome do grupo
        doc (App.Document): Documento onde criar o grupo (opcional, usa ActiveDocument)
        
    Returns:
        App.DocumentObjectGroup: O grupo criado ou encontrado
    """
    if doc is None:
        doc = App.activeDocument()
    
    if doc is None:
        return None
        
    group = doc.getObject(name)
    if group is None:
        group = doc.addObject("App::DocumentObjectGroup", name)
        
    return group


def findObjectLink(obj, doc=None):
    if doc is None:
        doc = App.activeDocument()
    for o in doc.Objects: 
        if hasattr(o, 'LinkedObject'):
            if o.LinkedObject == obj:
                return o 
    return None


def getSelectionPath(docName, objName, subObjName):
    val = []
    if (docName is None) or (docName == ''):
        if App.activeDocument():
            docName = App.activeDocument().Name
        else:
            return []
    val.append(docName)
    if objName and (objName != ''):
        val.append(objName)
        if subObjName and (subObjName != ''):
            for son in subObjName.split('.'):
                val.append(son)
    return val


def cloneObject(obj):
    container = obj.getParentGeoGroup()
    result = None
    if obj.Document and container:
        result = obj.Document.addObject('App::Link', obj.Name)
        result.LinkedObject = obj
        result.Label = obj.Label
        container.addObject(result)
        result.recompute()
        container.recompute()
        result.Document.recompute()
    return result 


def placeObjectToLCS(attObj, attLink, attDoc, attLCS):
    # Nota: makeExpressionDatum e makeAsmProperties precisam estar definidos
    # ou importados se forem usados. Por enquanto mantemos o placeholder.
    pass