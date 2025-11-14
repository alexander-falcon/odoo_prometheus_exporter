# -*- coding: utf-8 -*-

{
    'name': "Odoo Prometheus Exporter",
    'version': '16.0.1.0',
    'category': 'Monitoring',
    'summary': 'Exporter de métricas de Odoo para Prometheus',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
     
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'application': False,
    'author': "Alexander Falcon",
    'license': 'LGPL-3',
}
