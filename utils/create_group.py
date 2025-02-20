# Classe para a criar um group 
# Teste se já existe o grupo, se existir ele limpa, se não ele cria o grupo 
# author: Lucas Losinskas



def create_group(name:str, doc):
    group = ""
    if doc.getObject(name) is not None:
        group = doc.getObject(name)
        group.removeObjectsFromDocument()
        doc.removeObject(name)
        group = doc.addObject("App::DocumentObjectGroup", name)
    else:
        group = doc.addObject("App::DocumentObjectGroup", name)

    return group