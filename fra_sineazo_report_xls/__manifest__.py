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
    'name': "Fra Sineazo Report XLS",
    'summary': """Export to XLS a report of invoices and providers.""",
    'license': '',
    'author': "Quanam",
    'website': "https://www.quanam.com",
    'category': 'Survey',
    'version': '13.0.1',
    'depends': [
        'base',
        'account',
        'sale_management',
        'purchase'],
    'data': [
        'wizards/wizard_report_xls.xml',
    ],
    'installable': True,
    'auto_install': False
}
