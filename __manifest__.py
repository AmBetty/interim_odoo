# -*- coding: utf-8 -*-
{
    'name': 'Gestion Intérims',
    'version': '1.0',
    'category': 'Agents',
    'summary': 'Gérer les intérims',
    'description': "Agents",
    'depends': ['base', 'account', 'sale'],
    'data': [
        'views/interim.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
