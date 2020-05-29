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

from odoo import api, fields, models, exceptions, _
import xlwt
from io import BytesIO
import base64
from odoo.tools.misc import formatLang, format_date
import ast


class WizardReportXLS(models.TransientModel):
    _name = 'wizard.report.xls'
    _description = 'Report XLS'

    def _get_file_to_export(self):

        fl = BytesIO()
        wbk = xlwt.Workbook()
        partner_ids = self.env['res.partner']

        # Page FACTURAS STORE
        page_1 = self.style_page_1(wbk)
        partner_ids |= self.records_page_1(page_1)

        # Page FACTURAS RECIBIDAS
        page_2 = self.style_page_2(wbk)
        partner_ids |= self.records_page_2(page_2)

        # Page PROVEEDORES
        page_3 = self.style_page_3(wbk)
        self.records_page_3(page_3, partner_ids)

        wbk.save(fl)
        fl.seek(0)
        file = base64.encodebytes(fl.read())
        fl.close()
        return file

    def style_page_1(self, wbk):
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        borders = xlwt.Borders()
        borders.left = 4
        borders.right = 4
        borders.top = 4
        borders.bottom = 4
        bold_style.borders = borders
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        bold_style.alignment = alignment
        page_1 = wbk.add_sheet('FACTURAS EMITIDAS STORE',
                               cell_overwrite_ok=True)
        page_1.set_horz_split_pos(1)
        page_1.panes_frozen = True
        page_1.remove_splits = True
        page_1.col(0).width = 256 * 1
        page_1.col(1).width = 256 * 20
        page_1.col(3).width = 256 * 40
        page_1.col(5).width = 256 * 20
        page_1.col(7).width = 256 * 20
        page_1.col(9).width = 256 * 20
        page_1.col(11).width = 256 * 30
        page_1.write(0, 1, _('FACTURA'), bold_style)
        page_1.write(0, 2, _('DATA'), bold_style)
        page_1.write(0, 3, _('CLIENT'), bold_style)
        page_1.write(0, 4, _('BASE'), bold_style)
        page_1.write(0, 5, _('BASE EXENTA'), bold_style)
        page_1.write(0, 6, _('% IVA'), bold_style)
        page_1.write(0, 7, _('CUOTA IVA'), bold_style)
        page_1.write(0, 8, _('IRPF'), bold_style)
        page_1.write(0, 9, _('CUOTA IRPF'), bold_style)
        page_1.write(0, 10, _('TOTAL'), bold_style)
        page_1.write(0, 11, _('COBRADA EN'), bold_style)
        page_1.write(0, 12, _('FECHA'), bold_style)
        return page_1

    def style_page_2(self, wbk):
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        bold_style.alignment = alignment
        page_2 = wbk.add_sheet('FACTURAS RECIBIDAS',
                               cell_overwrite_ok=True)
        page_2.set_horz_split_pos(1)
        page_2.panes_frozen = True
        page_2.remove_splits = True
        page_2.col(0).width = 256 * 1
        page_2.col(1).width = 256 * 20
        page_2.col(3).width = 256 * 40
        page_2.col(5).width = 256 * 20
        page_2.col(7).width = 256 * 20
        page_2.col(9).width = 256 * 20
        page_2.col(11).width = 256 * 30
        page_2.write(0, 1, _('NO. FACTURA'), bold_style)
        page_2.write(0, 2, _('FECHA'), bold_style)
        page_2.write(0, 3, _('PROVEEDOR'), bold_style)
        page_2.write(0, 4, _('BASE'), bold_style)
        page_2.write(0, 5, _('BASE EXENTA'), bold_style)
        page_2.write(0, 6, _('% IVA'), bold_style)
        page_2.write(0, 7, _('CUOTA IVA'), bold_style)
        page_2.write(0, 8, _('IRPF'), bold_style)
        page_2.write(0, 9, _('CUOTA IRPF'), bold_style)
        page_2.write(0, 10, _('TOTAL'), bold_style)
        page_2.write(0, 11, _('COBRADA EN'), bold_style)
        page_2.write(0, 12, _('FECHA'), bold_style)
        return page_2

    def style_page_3(self, wbk):
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        bold_style.alignment = alignment
        page_3 = wbk.add_sheet('PROVEEDORES',
                               cell_overwrite_ok=True)
        page_3.set_horz_split_pos(1)
        page_3.panes_frozen = True
        page_3.remove_splits = True
        page_3.col(0).width = 256 * 1
        page_3.col(1).width = 256 * 50
        page_3.col(2).width = 256 * 30
        page_3.col(3).width = 256 * 30
        page_3.col(4).width = 256 * 40
        page_3.col(5).width = 256 * 30
        page_3.col(6).width = 256 * 20
        page_3.col(7).width = 256 * 20
        page_3.col(10).width = 256 * 30
        page_3.write(0, 1, _('NOMBRE'), bold_style)
        page_3.write(0, 2, _('DENOMINACION FISCAL'), bold_style)
        page_3.write(0, 3, _('CIF'), bold_style)
        page_3.write(0, 4, _('DIRECCION'), bold_style)
        page_3.write(0, 5, _('CIUDAD'), bold_style)
        page_3.write(0, 6, _('PROVINCIA'), bold_style)
        page_3.write(0, 7, _('PAIS'), bold_style)
        page_3.write(0, 8, _('C.P.'), bold_style)
        page_3.write(0, 9, _('% IVA'), bold_style)
        page_3.write(0, 10, _('COBRADA EN'), bold_style)
        page_3.write(0, 11, _('FECHA'), bold_style)
        return page_3

    def records_page_1(self, page_1):
        partner_ids = self.env['res.partner']
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        bold_style.alignment = alignment

        bold_style_num = xlwt.XFStyle()
        bold_style_num.font = font
        alignment2 = xlwt.Alignment()
        alignment2.horz = xlwt.Alignment.HORZ_RIGHT
        alignment2.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        bold_style_num.alignment = alignment2

        bold_style_percent = xlwt.XFStyle()
        bold_style_percent.font = font
        alignment3 = xlwt.Alignment()
        alignment3.horz = xlwt.Alignment.HORZ_RIGHT
        alignment3.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        bold_style_percent.alignment = alignment3
        bold_style_percent.num_format_str = '#,##0.00 %'

        bold_style_date = xlwt.XFStyle()
        bold_style_date.font = font
        alignment4 = xlwt.Alignment()
        alignment4.horz = xlwt.Alignment.HORZ_CENTER
        bold_style_date.alignment = alignment4
        bold_style_date.num_format_str = 'DD/MM/YY'

        domain = [
            ('type', '=', 'out_invoice')
        ]
        invoice_out_ids = self.env['account.move'].search(domain,
                                                          order='name ASC')
        partner_ids |= invoice_out_ids.mapped('partner_id')

        row = 1
        for invoice in invoice_out_ids:
            currency = invoice.currency_id.symbol
            if invoice.currency_id.position == 'after':
                bold_style_num.num_format_str = '#,##0.00 %s' % currency
            else:
                bold_style_num.num_format_str = '%s #,##0.00' % currency

            create_date = format_date(self.env, fields.Date.to_string(
                invoice.create_date),
                               date_format='dd/MM/YYYY')
            iva = 0
            irpf = 0
            Tax = self.env['account.tax']
            Group = self.env['account.tax.group']
            for group in invoice.amount_by_group:
                array = []
                array.append(group)
                new_array = [x for xs in array for x in xs]

                group_id = Group.browse(new_array[6])
                iva_domain = [
                    ('tax_group_id', '=', group_id.id),
                    ('description', 'ilike', 'IVA'),
                ]
                iva_tax_id = Tax.search(iva_domain, limit=1)
                if iva_tax_id:
                    iva = iva_tax_id.amount / 100

                irpf_domain = [
                    ('tax_group_id', '=', group_id.id),
                    ('description', 'ilike', 'IRPF'),
                ]
                irpf_tax_id = Tax.search(irpf_domain, limit=1)
                if irpf_tax_id:
                    irpf = irpf_tax_id.amount / 100 * -1

            payment_date = ''
            invoice_payments_widget = invoice.invoice_payments_widget
            if invoice_payments_widget != 'false':
                invoice_payments_widget = invoice_payments_widget.replace(
                    'false', 'False')
                invoice_payments_widget = invoice_payments_widget.replace(
                    'true', 'True')
                invoice_payments_widget = invoice_payments_widget.replace(
                    'null', 'None')
                payments = ast.literal_eval(invoice_payments_widget).get('content', [])
                if payments:
                    index = len(payments) - 1
                    payment = payments[index]
                    if payment.get('date', False):
                        payment_date = format_date(
                            self.env,
                            payment.get('date', False),
                            date_format='dd/MM/YYYY')

            formula_cuota_iva = "E%d*G%d" % (row+1, row+1)
            formula_cuota_rpf = "E%d*I%d" % (row+1, row+1)
            formula_total = "E%d+F%d+H%d-J%d" % (row+1, row+1, row+1, row+1)
            page_1.write(row, 1, invoice.name, bold_style)
            page_1.write(row, 2, create_date, bold_style_date)
            page_1.write(row, 3, invoice.partner_id.name, bold_style)
            page_1.write(row, 4, invoice.amount_untaxed, bold_style_num)
            page_1.write(row, 5, 0.0, bold_style_num)
            page_1.write(row, 6, iva, bold_style_percent)
            page_1.write(row, 7, xlwt.Formula(formula_cuota_iva), bold_style_num)
            page_1.write(row, 8, irpf, bold_style_percent)
            page_1.write(row, 9, xlwt.Formula(formula_cuota_rpf), bold_style_num)
            page_1.write(row, 10, xlwt.Formula(formula_total), bold_style_num)
            page_1.write(row, 11, '', bold_style)
            page_1.write(row, 12, payment_date, bold_style_date)
            row += 1
        return partner_ids

    def records_page_2(self, page_2):
        partner_ids = self.env['res.partner']
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.wrap = 1
        bold_style.alignment = alignment

        bold_style_num = xlwt.XFStyle()
        bold_style_num.font = font
        alignment2 = xlwt.Alignment()
        alignment2.horz = xlwt.Alignment.HORZ_RIGHT
        bold_style_num.alignment = alignment2

        bold_style_percent = xlwt.XFStyle()
        bold_style_percent.font = font
        alignment3 = xlwt.Alignment()
        alignment3.horz = xlwt.Alignment.HORZ_RIGHT
        bold_style_percent.alignment = alignment3
        bold_style_percent.num_format_str = '#,##0.00 %'

        bold_style_date = xlwt.XFStyle()
        bold_style_date.font = font
        alignment4 = xlwt.Alignment()
        alignment4.horz = xlwt.Alignment.HORZ_CENTER
        bold_style_date.alignment = alignment4
        bold_style_date.num_format_str = 'DD/MM/YY'

        domain = [
            ('type', '=', 'in_invoice')
        ]
        invoice_out_ids = self.env['account.move'].search(domain,
                                                          order='name ASC')
        partner_ids |= invoice_out_ids.mapped('partner_id')

        row = 1
        for invoice in invoice_out_ids:
            currency = invoice.currency_id.symbol
            if invoice.currency_id.position == 'after':
                bold_style_num.num_format_str = '#,##0.00 %s' % currency
            else:
                bold_style_num.num_format_str = '%s #,##0.00' % currency

            create_date = format_date(self.env, fields.Date.to_string(
                invoice.create_date),
                                      date_format='dd/MM/YYYY')

            iva = 0
            irpf = 0
            Tax = self.env['account.tax']
            Group = self.env['account.tax.group']
            for group in invoice.amount_by_group:
                array = []
                array.append(group)
                new_array = [x for xs in array for x in xs]

                group_id = Group.browse(new_array[6])
                iva_domain = [
                    ('tax_group_id', '=', group_id.id),
                    ('description', 'ilike', 'IVA'),
                ]
                iva_tax_id = Tax.search(iva_domain, limit=1)
                if iva_tax_id:
                    iva = iva_tax_id.amount / 100

                irpf_domain = [
                    ('tax_group_id', '=', group_id.id),
                    ('description', 'ilike', 'IRPF'),
                ]
                irpf_tax_id = Tax.search(irpf_domain, limit=1)
                if irpf_tax_id:
                    irpf = irpf_tax_id.amount / 100 * -1

            payment_date = ''
            invoice_payments_widget = invoice.invoice_payments_widget
            if invoice_payments_widget != 'false':
                invoice_payments_widget = invoice_payments_widget.replace(
                    'false', 'False')
                invoice_payments_widget = invoice_payments_widget.replace(
                    'true', 'True')
                invoice_payments_widget = invoice_payments_widget.replace(
                    'null', 'None')
                payments = ast.literal_eval(invoice_payments_widget).get(
                    'content', [])
                if payments:
                    index = len(payments) - 1
                    payment = payments[index]
                    if payment.get('date', False):
                        payment_date = format_date(
                            self.env,
                            payment.get('date', False),
                            date_format='dd/MM/YYYY')

            formula_cuota_iva = "E%d*G%d" % (row+1, row+1)
            formula_cuota_rpf = "E%d*I%d" % (row+1, row+1)
            formula_total = "E%d+F%d+H%d-J%d" % (row+1, row+1, row+1, row+1)
            page_2.write(row, 1, invoice.name, bold_style)
            page_2.write(row, 2, create_date, bold_style_date)
            page_2.write(row, 3, invoice.partner_id.name, bold_style)
            page_2.write(row, 4, invoice.amount_untaxed, bold_style_num)
            page_2.write(row, 5, 0.0, bold_style_num)
            page_2.write(row, 6, iva, bold_style_percent)
            page_2.write(row, 7, xlwt.Formula(formula_cuota_iva), bold_style_num)
            page_2.write(row, 8, irpf, bold_style_percent)
            page_2.write(row, 9, xlwt.Formula(formula_cuota_rpf), bold_style_num)
            page_2.write(row, 10,  xlwt.Formula(formula_total), bold_style_num)
            page_2.write(row, 11, '', bold_style)
            page_2.write(row, 12, payment_date, bold_style_date)
            row += 1
        return partner_ids

    def records_page_3(self, page_3, partner_ids):
        font = xlwt.Font()
        bold_style = xlwt.XFStyle()
        font.name = 'Calibri'
        font.height = 20 * 11
        bold_style.font = font
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.wrap = 1
        bold_style.alignment = alignment

        bold_style_num = xlwt.XFStyle()
        bold_style_num.font = font
        alignment2 = xlwt.Alignment()
        alignment2.horz = xlwt.Alignment.HORZ_RIGHT
        bold_style_num.alignment = alignment2

        bold_style_percent = xlwt.XFStyle()
        bold_style_percent.font = font
        alignment3 = xlwt.Alignment()
        alignment3.horz = xlwt.Alignment.HORZ_RIGHT
        bold_style_percent.alignment = alignment3
        bold_style_percent.num_format_str = '#,##0.00 %'

        bold_style_date = xlwt.XFStyle()
        bold_style_date.font = font
        alignment4 = xlwt.Alignment()
        alignment4.horz = xlwt.Alignment.HORZ_CENTER
        bold_style_date.alignment = alignment4
        bold_style_date.num_format_str = 'DD/MM/YY'

        provider_ids = partner_ids

        row = 1
        for provider in provider_ids:
            today = fields.Date.today()
            date = format_date(self.env, fields.Date.to_string(today),
                               date_format='dd/MM/YYYY')
            addr = []
            address = ''
            if provider.street:
                addr.append(provider.street)
            if provider.street2:
                addr.append(provider.street2)
            if addr:
                address = ', '.join(addr)
            page_3.write(row, 1, provider.name, bold_style)
            page_3.write(row, 2, '', bold_style_date)
            page_3.write(row, 3, provider.vat or '', bold_style)
            page_3.write(row, 4, address, bold_style)
            page_3.write(row, 5, provider.city or '', bold_style)
            page_3.write(row, 6, provider.state_id.name or '', bold_style)
            page_3.write(row, 7, provider.country_id.name or '', bold_style)
            page_3.write(row, 8, provider.zip or '', bold_style)
            page_3.write(row, 9, 0.0, bold_style_percent)
            page_3.write(row, 10, '', bold_style)
            page_3.write(row, 11, '', bold_style_date)
            row += 1

    def generate_xls(self):
        file = self._get_file_to_export()
        wizard_id = self.env['wizard.report.download.xls'].create(
            {
                'file_name': _('REGISTRO FRA SINEAZO.xls'),
                'file': file
            }
        )
        return {
            'name': _('Sineazo Report'),
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref(
                'fra_sineazo_report_xls.wizard_report_download_xls').id,
            'res_id': wizard_id.id,
            'view_mode': 'form',
            'res_model': 'wizard.report.download.xls',
            'target': 'new',
        }


class WizardReportDownloadXLS(models.TransientModel):
    _name = 'wizard.report.download.xls'
    _description = 'Report Download XLS'

    file = fields.Binary(
        'File',
        help="File to export"
    )
    file_name = fields.Char(
        string="File name",
        size=64
    )

