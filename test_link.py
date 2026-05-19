import FreeCAD as App
import os

try:
    print("Test started")
    doc1 = App.newDocument('Doc1')
    doc2 = App.newDocument('Doc2')
    
    part2 = doc2.addObject('App::Part', 'Part2')
    box = doc2.addObject('Part::Box', 'Box')
    part2.addObject(box)
    
    doc2.recompute()
    doc2.saveAs(os.path.abspath('test_doc2.FCStd'))
    doc1.saveAs(os.path.abspath('test_doc1.FCStd'))
    
    print("Creating link to part...")
    link = doc1.addObject('App::Link', 'Link')
    link.LinkedObject = part2
    print("Link target set to part!")
    
except Exception as e:
    import traceback
    print("Error:", str(e))
    traceback.print_exc()
