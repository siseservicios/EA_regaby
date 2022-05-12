{
    'name': 'REPORT MANAGEMENT DEBT',
    'version': '1.0.0.0.0',
    'category': 'Base',
    'sequence': 11,
    'summary': ''' 
        This module creates a personalized debt report for the client.
    ''',
    'author': 'Romina Bazan',
    'license': 'AGPL-3',
    'images': [
    ],
    'depends': [
        'base',
        'account',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/report_management_debt_view.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
