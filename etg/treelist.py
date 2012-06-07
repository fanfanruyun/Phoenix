#---------------------------------------------------------------------------
# Name:        etg/treelist.py
# Author:      Robin Dunn
#
# Created:     06-Jun-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_adv"
NAME      = "treelist"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxTreeListItem",
           "wxTreeListItemComparator",
           "wxTreeListCtrl",
           "wxTreeListEvent",
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/treelist.h>')
    module.find('wxTreeListEventHandler').ignore()
    module.find('wxTreeListItems').ignore()
    
    module.insertItem(0, etgtools.WigCode("""\
        // forward declare
        class wxDataViewCtrl;
        """))
    

    #-----------------------------------------------------------------
    c = module.find('wxTreeListItem')
    assert isinstance(c, etgtools.ClassDef)
    c.addCppMethod('int', '__nonzero__', '()', """\
        return self->IsOk();
        """)
     
     
    #-----------------------------------------------------------------
    c = module.find('wxTreeListItemComparator')
    c.addPrivateCopyCtor()
     
    
    #-----------------------------------------------------------------
    c = module.find('wxTreeListCtrl')
    tools.fixWindowClass(c)
    
    module.addGlobalStr('wxTreeListCtrlNameStr', c)
    
    # transfer ownership of some parameters
    c.find('AssignImageList.imageList').transfer = True
    c.find('SetItemData.data').transfer = True
    c.find('AppendItem.data').transfer = True
    c.find('InsertItem.data').transfer = True
    c.find('PrependItem.data').transfer = True
    
    
    # Replace GetSelections with an implementation that returns a Python list
    c.find('GetSelections').ignore()
    c.addCppMethod('PyObject*', 'GetSelections', '()',
        doc="""\
            Returns a list of all selected items. This method can be used in 
            both single and multi-selection case.""",
        body="""\
            unsigned count;
            wxTreeListItems items;
            count = self->GetSelections(items);
            
            wxPyThreadBlocker blocker;
            PyObject* list = PyList_New(count);
            for (size_t i=0; i<count; i++) {
                wxTreeListItem* item = new wxTreeListItem(items[i]);
                PyObject* obj = wxPyConstructObject((void*)item, wxT("wxTreeListItem"), true);
                PyList_SET_ITEM(list, i, obj); // PyList_SET_ITEM steals a reference
            }            
            return list;
        """)
    
    # Set output parameter flags
    c.find('GetSortColumn.col').out = True
    c.find('GetSortColumn.ascendingOrder').out = True
    
    # Replace NO_IMAGE with wxTreeListCtrl::NO_IMAGE in parameter default values
    for item in c.allItems():
        if isinstance(item, etgtools.ParamDef) and item.default == 'NO_IMAGE':
            item.default = 'wxTreeListCtrl::NO_IMAGE'
        
    #-----------------------------------------------------------------
    c = module.find('wxTreeListEvent')
    tools.fixEventClass(c)
    
    c.addPyCode("""\
        EVT_TREELIST_SELECTION_CHANGED = wx.PyEventBinder( wxEVT_COMMAND_TREELIST_SELECTION_CHANGED )
        EVT_TREELIST_ITEM_EXPANDING =    wx.PyEventBinder( wxEVT_COMMAND_TREELIST_ITEM_EXPANDING )
        EVT_TREELIST_ITEM_EXPANDED =     wx.PyEventBinder( wxEVT_COMMAND_TREELIST_ITEM_EXPANDED )
        EVT_TREELIST_ITEM_CHECKED =      wx.PyEventBinder( wxEVT_COMMAND_TREELIST_ITEM_CHECKED )
        EVT_TREELIST_ITEM_ACTIVATED =    wx.PyEventBinder( wxEVT_COMMAND_TREELIST_ITEM_ACTIVATED )
        EVT_TREELIST_ITEM_CONTEXT_MENU = wx.PyEventBinder( wxEVT_COMMAND_TREELIST_ITEM_CONTEXT_MENU )
        EVT_TREELIST_COLUMN_SORTED =     wx.PyEventBinder( wxEVT_COMMAND_TREELIST_COLUMN_SORTED )        
        """)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

