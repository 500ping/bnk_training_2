from odoo import models, fields, api, _

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_date_due')
    def _is_overdue_compute(self):
        for rec in self:
            if rec.invoice_date_due and rec.invoice_date_due < fields.Date.today()\
                    and rec.state == 'posted'\
                    and rec.invoice_payment_state != 'paid':
                rec.is_overdue = True
            else:
                rec.is_overdue = False

    @api.depends('invoice_date_due', 'amount_residual')
    def _overdue_interest_compute(self):
        for rec in self:
            if rec.is_overdue:
                overdue_dates = fields.Date.today() - rec.invoice_date_due
                rec.overdue_interest = (rec.amount_residual * 15 / 100) * overdue_dates.days
            else:
                rec.overdue_interest = 0.0

    # Custom fields
    is_overdue = fields.Boolean(string="Overdue", store=True, compute=_is_overdue_compute, default=False)
    overdue_interest = fields.Monetary(string='Overdue Interest', compute='_overdue_interest_compute', currency_field='company_currency_id')

    def action_test_inherit(self):
        for rec in self:
            print(rec.is_overdue)
            print(rec.amount_residual)

            print(rec.overdue_interest)