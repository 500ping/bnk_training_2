from odoo import models, fields, api, _

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_date_due', 'state', 'invoice_payment_state', 'payment_history_ids')
    def _is_overdue_compute(self):
        for rec in self:
            if rec.invoice_date_due and rec.invoice_date_due < fields.Date.today()\
                    and rec.state == 'posted'\
                    and rec.invoice_payment_state != 'paid':
                rec.is_overdue = True
            elif rec.invoice_date_due and rec.invoice_date_due < fields.Date.today()\
                    and rec.state == 'posted'\
                    and rec.invoice_payment_state == 'paid':
                temp = False
                # for payment in rec.payment_history_ids:
                #     if payment.payment_date > rec.invoice_date_due:
                #         temp = True
                #         break
                rec.is_overdue = temp
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


    def _payment_history_ids_compute(self):
        payments_history = self.env['account.payment'].search([('invoice_ids', '=', self.id)])
        self.payment_history_ids = payments_history


    # Custom fields
    is_overdue = fields.Boolean(string="Overdue", store=True, compute=_is_overdue_compute, default=False)
    overdue_interest = fields.Monetary(string='Overdue Interest', compute='_overdue_interest_compute', currency_field='company_currency_id')

    payment_history_ids = fields.Many2many('account.payment', string='Payments history', compute='_payment_history_ids_compute')

    def action_test_inherit(self):
        for rec in self:
            print(rec.is_overdue)
            # print(rec.amount_residual)
            # print(rec.overdue_interest)
            # print(self.env['account.payment'].search([('invoice_ids', '=', rec.id)]))

            print(rec.invoice_date_due)

            for payment in rec.payment_history_ids:
                print(payment.payment_date)

                if payment.payment_date > rec.invoice_date_due:
                    print("1")

