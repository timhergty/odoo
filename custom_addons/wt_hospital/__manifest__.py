{
    'name': 'Hospital Management System',
    'version': '9.1',
    'category': 'Extra Tools',
    'sequence': -100,
    'summary': 'System for managing Hospital Operations',
    'website': 'https://www.odoo.com/',
    'images': [],
    'depends': ['sale', 'mail', 'board', 'website'],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'author': 'Wasike Timothy',
    'license': 'LGPL-3',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/data.xml',
        'data/cron.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        # 'views/lab.xml',
        # 'views/billing.xml',
        'views/sale_order.xml',
        'views/patient_template.xml',
        'views/portal_template.xml',
        'views/doctor_template.xml',
        # 'views/dashboard.xml',
        'views/menu.xml',
    ]
}
