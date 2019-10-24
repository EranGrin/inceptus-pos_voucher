# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

{
    'name': "POS Voucher",

    'summary': """
        POS Voucher""",

    'description': """
        POS Voucher
    """,

    'author': "Inceptus.io",
    'website': "http://www.inceptus.io",
    'category': 'POS',
    'version': '1.0',

    'depends': ['ies_base_redeem', 'ies_base'],

    'data': [
        'wizard/generate_voucher_view.xml',
        'views/voucher_view.xml',
        'views/pos_view.xml',
    ],

    'qweb': ['static/src/xml/*.xml'],

    'installable': True,
    'auto_install': False,
    'application': True,
}
