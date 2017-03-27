# -*- coding: utf-8 -*-
{
    'name': "Employees tree view",

    'summary': """
        The tree representation of the employees structure
    """,

    'description': """
        The tree representation of the employees structure
    """,

    'author': "Ihar Niamilentsau",
    'website': "https://scnsoft.com",

    'category': 'Human Resources',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/etv_menu.xml',
        'views/etv_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
