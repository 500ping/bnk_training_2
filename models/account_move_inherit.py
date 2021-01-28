from odoo import models, fields, api, _
import json

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    # @api.depends('invoice_date_due', 'state', 'invoice_payment_state')
    # def _has_overdue_interest_compute(self):
    #     for rec in self:
    #         if rec.invoice_date_due and rec.invoice_date_due < fields.Date.today()\
    #                 and rec.state == 'posted'\
    #                 and rec.invoice_payment_state != 'paid':
    #             rec.has_overdue_interest = True
    #         elif rec.invoice_date_due and rec.invoice_date_due < fields.Date.today()\
    #                 and rec.state == 'posted'\
    #                 and rec.invoice_payment_state == 'paid':
    #             temp = False
    #             # for payment in rec.payment_history_ids:
    #             #     if payment.payment_date > rec.invoice_date_due:
    #             #         temp = True
    #             #         break
    #             rec.has_overdue_interest = temp
    #         else:
    #             rec.has_overdue_interest = False


    # @api.depends('invoice_date_due', 'amount_residual', '')
    # def _overdue_interest_compute(self):
    #     for rec in self:
    #         if rec.has_overdue_interest:
    #             overdue_dates = fields.Date.today() - rec.invoice_date_due
    #             rec.overdue_interest = (rec.amount_residual * 15 / 100) * overdue_dates.days
    #         else:
    #             rec.overdue_interest = 0.0


    def _payment_history_ids_compute(self):
        # payments_history = self.env['account.payment'].search([('invoice_ids', '=', self.id)])
        # self.payment_history_ids = payments_history
        for rec in self:
            invoice_payments_info = json.loads(rec.invoice_payments_widget)
            if invoice_payments_info:
                payment_ids = [content['account_payment_id'] for content in invoice_payments_info['content']]
                self.payment_history_ids = self.env['account.payment'].browse(payment_ids)
            else:
                self.payment_history_ids = False

    # Custom fields
    has_overdue_interest = fields.Boolean(string="Has Overdue Interest", default=False)
    overdue_interest_at_check_date = fields.Monetary(string='Overdue Interest At Check Date', currency_field='company_currency_id', default=0.0)
    overdue_check_date = fields.Date(string='Overdue Check Date')

    payment_history_ids = fields.Many2many('account.payment', string='Payments history', compute='_payment_history_ids_compute')

    def action_test_inherit(self):
        print('Today:', fields.Date.today())
        for rec in self:
            print(rec.has_overdue_interest)
            print(rec.amount_residual)

            print('Due date:',rec.invoice_date_due)

            invoice_payments = json.loads(rec.invoice_payments_widget)

            for content in invoice_payments['content']:
                print(content['account_payment_id'])

            print(rec.get_overdue_total())

    def get_invoice_payments(self):
        for rec in self:
            invoice_payments_info = json.loads(rec.invoice_payments_widget)
            if invoice_payments_info:
                payment_ids = [content['account_payment_id'] for content in invoice_payments_info['content']]
                return self.env['account.payment'].browse(payment_ids)

    def get_payments_not_overdue(self):
        payments = self.get_invoice_payments()
        payments_not_overdue = payments.filtered(lambda payment: payment.payment_date <= self.invoice_date_due)
        return payments_not_overdue

    def get_payments_overdue(self):
        payments = self.get_invoice_payments()
        payments_overdue = payments.filtered(lambda payment: payment.payment_date > self.invoice_date_due)
        return payments_overdue

    def get_overdue_total(self):
        overdue_total = self.amount_total

        payments_not_overdue = self.get_payments_not_overdue()

        if len(payments_not_overdue) == 0:
            return overdue_total
        else:
            for payment in payments_not_overdue:
                overdue_total -= payment.amount
            return overdue_total

    def calculate_overdue_interest(self):
        overdue_total = self.get_overdue_total()






