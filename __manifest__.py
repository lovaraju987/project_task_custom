# -*- coding: utf-8 -*-
{
    'name': "project_task_custom",

    'summary': "field service related project customization",

    'description': """
for field service project added the following features, 1) slot model, 2) assignee phone number compute feild 3) supporting technicians field
    """,

    'author': "OneTo7 Safety Nets",
    'website': "https://www.oneto7safetynets.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'summary': 'Enhance project tasks with slot allocation for field service tasks',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['project', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/field_service_slot_data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'installable': True,
    'application': False,
}

