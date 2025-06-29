# -*- coding: utf-8 -*-
{
    'name': "mbf crm whatsapp",

    'summary': """
    Integrasi menu CRM dan Whatspass Server    

    """,

    'description': """
        Komunikasi dengan customer dengan whatsapp baik menerima maupun mengirim pesan
        sehingga akan memudahkan dalam monitoring hubungan customer
    """,

    'author': "Fikri Software",
    'website': "http://www.fikrisoftware.my.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm'],    
    'data': [
        'security/ir.model.access.csv',
        # 'data/ir_config_parameter.xml',
        # 'data/ir.whatsapp_server.xml',
        'views/crm_lead_view.xml',
        'views/ir_whatsapp_server.xml',
        'views/menuitem_view.xml',
        'wizard/whatsapp_message_view.xml',
        'views/css_loader.xml',
    ],
    'qweb': ['static/src/xml/chat_bubble_template.xml'],  # Optional

    # 'assets': {
    #     'web.assets_backend': [
    #         'mbf_crm_whatsapp/static/src/css/message.css',
    # ],
    # },
    # always loaded
    # only loaded in demonstration mode
    'demo': [],
}
