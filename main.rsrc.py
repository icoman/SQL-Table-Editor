{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':u'Standard Template with no menus',
          'size':(944, 649),

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':u'File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileAbout',
                   'label':u'About',
                   'command':'about',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'Button', 
    'name':'Refresh', 
    'position':(740, 85), 
    'command':'refresh', 
    'label':'Refresh', 
    },

{'type':'Button', 
    'name':'deleteRecord', 
    'position':(625, 85), 
    'command':'delrec', 
    'label':'Delete Record', 
    },

{'type':'Button', 
    'name':'appendRecord', 
    'position':(505, 85), 
    'command':'addrec', 
    'label':'Append Record', 
    },

{'type':'TextField', 
    'name':'filter', 
    'position':(70, 85), 
    'size':(410, -1), 
    'text':'filter', 
    },

{'type':'StaticText', 
    'name':'Filter', 
    'position':(20, 90), 
    'size':(44, -1), 
    'alignment':'right', 
    'text':'Filter:', 
    },

{'type':'StaticText', 
    'name':'Table', 
    'position':(590, 60), 
    'size':(47, -1), 
    'alignment':'right', 
    'text':'Table:', 
    },

{'type':'StaticText', 
    'name':'DSN', 
    'position':(20, 60), 
    'size':(42, -1), 
    'alignment':'right', 
    'text':'DSN:', 
    },

{'type':'ComboBox', 
    'name':'tableList', 
    'position':(645, 55), 
    'size':(240, -1), 
    'items':[], 
    'text':'tableList', 
    },

{'type':'ComboBox', 
    'name':'DSNList', 
    'position':(70, 55), 
    'size':(495, -1), 
    'items':[], 
    'text':'DSNList', 
    },

{'type':'StaticText', 
    'name':'title', 
    'position':(120, 10), 
    'size':(652, 32), 
    'alignment':'center', 
    'font':{'faceName': u'Segoe UI', 'family': 'sansSerif', 'size': 14}, 
    'text':'title', 
    },

{'type':'Grid', 
    'name':'myGrid', 
    'position':(10, 120), 
    'size':(900, 450), 
    },

] # end components
} # end background
] # end backgrounds
} }
