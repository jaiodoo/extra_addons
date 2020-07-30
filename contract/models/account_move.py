# Copyright 2018 ACSONE SA/NV.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    def create_contract_from_invoice(self):
        self.ensure_one()
        if self.type in ['in_invoice', 'in_refund']:
            contract = self.env['contract.contract'].search(
                [
                    ('partner_id', '=', self.partner_id.id),
                    ('active', '=', True),
                    ('contract_type', '=', 'purchase'),

                ]
            )
        else:
            contract = self.env['contract.contract'].search(
                [
                    ('partner_id', '=', self.partner_id.id),
                    ('active', '=', True),
                    ('contract_type', '=', 'sale'),

                ]
            )
        step = 'step2' if contract else 'step1'
        ctx = self.env.context.copy()
        ctx.update(
            {
                'default_invoice_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_state': step,
                'default_contract_id': contract.id,
            }
        )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.contract.create',
            'name': _('Contract Creation'),
            'view_mode': 'form',
            'context': ctx,
            'target': 'new',
            'views': [(False, "form")],
        }
