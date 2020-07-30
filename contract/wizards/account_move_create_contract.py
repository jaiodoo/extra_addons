# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AcountMoveContract(models.TransientModel):

    _name = 'account.move.contract.create'
    _description = "Create Contract From Invoice Wizard"

    invoice_id = fields.Many2one(
        'account.move'
    )
    partner_id = fields.Many2one(
        'res.partner'
    )
    creation_type = fields.Selection(
        [
            ('add', 'Addition'),
            ('replace', 'Replace')
        ],
        default='replace'
    )
    state = fields.Selection(
        [
            ('step1', 'Step 1'),
            ('step2', 'Step 2'),
            ('step3', 'Step 3'),
        ],
        default='step1'
    )
    code = fields.Char(
        string="Reference",
    )
    date_start = fields.Date(
        string='Date Start',
        required=True,
        default=lambda self: fields.Date.context_today(self),
    )
    date_end = fields.Date(string='Date End', index=True)
    recurring_rule_type = fields.Selection(
        [
            ('daily', 'Day(s)'),
            ('weekly', 'Week(s)'),
            ('monthly', 'Month(s)'),
            ('monthlylastday', 'Month(s) last day'),
            ('quarterly', 'Quarter(s)'),
            ('semesterly', 'Semester(s)'),
            ('yearly', 'Year(s)'),
        ],
        default='monthly',
        string='Recurrence',
        help="Specify Interval for automatic invoice generation.",
        required=True,
    )
    recurring_interval = fields.Integer(
        default=1,
        string='Invoice Every',
        help="Invoice every (Days/Week/Month/Year)",
        required=True,
    )
    contract_id = fields.Many2one(
        'contract.contract'
    )

    def create_contract(self):
        for wizard in self:
            type_invoice = wizard.invoice_id.type
            if type_invoice in ['in_invoice', 'in_refund']:
                contract = self.contract_id or self.env[
                    'contract.contract'
                ].search(
                    [
                        ('partner_id', '=', wizard.partner_id.id),
                        ('active', '=', True),
                        ('contract_type', '=', 'purchase'),

                    ]
                )
                if contract:
                    self.contract_id = contract
                    return wizard.goto_step2()
                else:
                    self.create_new_contract(type='purchase')
            else:
                contract = self.contract_id or self.env[
                    'contract.contract'
                ].search(
                    [
                        ('partner_id', '=', wizard.partner_id.id),
                        ('active', '=', True),
                        ('contract_type', '=', 'sale'),

                    ]
                )
                if contract:
                    self.contract_id = contract
                    return wizard.goto_step2()
                else:
                    self.create_new_contract()
        return True

    def goto_step2(self):
        self.ensure_one()
        self.state = 'step2'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.contract.create',
            'res_id': self.id,
            'name': _('Contract Creation'),
            'view_mode': 'form',
            'target': 'new',
            'views': [(False, "form")],
        }

    def goto_step1(self):
        self.ensure_one()
        self.state = 'step1'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.contract.create',
            'res_id': self.id,
            'name': _('Contract Creation'),
            'view_mode': 'form',
            'target': 'new',
            'views': [(False, "form")],
        }

    def goto_step3(self):
        self.ensure_one()
        self.state = 'step3'
        self._finish_creation()
        return True

    def _finish_creation(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update({'force_cancel': True})
        if self.creation_type == 'replace':
            self.contract_id.contract_line_ids.with_context(ctx).cancel()
            self.contract_id.contract_line_ids.unlink()
        for line in self.invoice_id.invoice_line_ids:
            self.env['contract.line'].create(
                self._prepare_create_invoice_line(self.contract_id, line)
            )

        return True

    def _prepare_create_invoice_line(self, contract, line):
        values = {
            'contract_id': contract.id,
            'name': line.product_id.description or 'New',
            'date_start': self.date_start,
            'date_end': self.date_end,
            'product_id': line.product_id.id,
            'price_unit': line.price_unit,
            'discount': line.discount,
            'recurring_rule_type': self.recurring_rule_type,
            'recurring_interval': self.recurring_interval,

        }
        contract_line = self.env['contract.line'].new(values)
        contract_line._onchange_product_id()
        contract_line._update_recurring_next_date()
        vals = contract_line._convert_to_write(contract_line._cache)
        vals.update(
            {
                'price_unit': line.price_unit,
            }
        )
        return vals

    def create_new_contract(self, type='sale'):
        self.ensure_one()
        contract = self.env['contract.contract'].create(
            {
                'partner_id': self.partner_id.id,
                'contract_type': type,
                'name': 'Automatic Contract for %s' % self.partner_id.name,
                'code': self.code,

            }
        )
        for line in self.invoice_id.invoice_line_ids:
            self.env['contract.line'].create(
                self._prepare_create_invoice_line(contract, line)
            )

        return True


