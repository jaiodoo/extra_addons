##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 - Quanam
#    GFL Base Features
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Recurring - Contracts Management',
    'version': '13.0.0.0.0',
    'category': 'Contract Management',
    'license': 'AGPL-3',
    'author': "OpenERP SA, "
              "Tecnativa, "
              "LasLabs, "
              "Odoo Community Association (OCA)",
    'depends': ['base', 'account', 'product'],
    "external_dependencies": {"python": ["dateutil"]},
    'data': [
        'security/groups.xml',
        'security/contract_tag.xml',
        'security/ir.model.access.csv',
        'security/contract_security.xml',
        'security/contract_terminate_reason.xml',
        'report/report_contract.xml',
        'report/contract_views.xml',
        'data/contract_cron.xml',
        'data/contract_renew_cron.xml',
        'data/mail_template.xml',
        'data/ir_ui_menu.xml',
        'wizards/contract_line_wizard.xml',
        'wizards/contract_manually_create_invoice.xml',
        'wizards/contract_contract_terminate.xml',
        'views/contract_tag.xml',
        'views/assets.xml',
        'views/abstract_contract_line.xml',
        'views/contract.xml',
        'views/contract_line.xml',
        'views/contract_template.xml',
        'views/contract_template_line.xml',
        'views/res_partner_view.xml',
        'views/res_config_settings.xml',
        'views/contract_terminate_reason.xml',
    ],
    'installable': True,
}
