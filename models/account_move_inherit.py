from odoo import models, fields, api, _
import json

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

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
    overdue_interest_rate = fields.Integer(string="Overdue Interest Rate (%)", default=10)
    # has_overdue_interest = fields.Boolean(string="Has Overdue Interest", default=False)
    overdue_interest_at_check_date = fields.Monetary(string='Overdue Interest At Check Date', currency_field='company_currency_id', default=0.0)
    overdue_check_date = fields.Date(string='Overdue Check Date')

    payment_history_ids = fields.Many2many('account.payment', string='Payments history', compute='_payment_history_ids_compute')

    def action_test_inherit(self):
        print('Today:', fields.Date.today())
        for rec in self:
            print(rec.amount_residual)

            print('Due date:',rec.invoice_date_due)

            invoice_payments = json.loads(rec.invoice_payments_widget)

            for content in invoice_payments['content']:
                print(content['account_payment_id'])

            print('Overdue Total:',rec.get_overdue_total())

            overdue_dates = fields.Date.today() - rec.invoice_date_due
            print((fields.Date.today() - rec.invoice_date_due).days)

    def get_invoice_payments(self):
        for rec in self:
            invoice_payments_info = json.loads(rec.invoice_payments_widget)
            if invoice_payments_info:
                payment_ids = [content['account_payment_id'] for content in invoice_payments_info['content']]
                return self.env['account.payment'].browse(payment_ids)

    def get_payments_not_overdue(self):
        payments = self.get_invoice_payments()

        if not payments:
            return False

        payments_not_overdue = payments.filtered(lambda payment: payment.payment_date <= self.invoice_date_due)
        return payments_not_overdue

    def get_payments_overdue(self):
        payments = self.get_invoice_payments()

        if not payments:
            return False

        payments_overdue = payments.filtered(lambda payment: payment.payment_date > self.invoice_date_due).sorted('payment_date')
        return payments_overdue

    def get_overdue_total(self):
        overdue_total = self.amount_total

        payments_not_overdue = self.get_payments_not_overdue()

        if not payments_not_overdue:
            return overdue_total
        else:
            for payment in payments_not_overdue:
                overdue_total -= payment.amount
            return overdue_total

    def calculate_overdue_interest(self):
        for rec in self:
            overdue_total = rec.get_overdue_total()
            overdue_interest = 0.0

            payments_overdue = rec.get_payments_overdue()

            if payments_overdue:
                for payment in payments_overdue:
                    overdue_interest += (overdue_total * rec.overdue_interest_rate / 100) * ( (payment.payment_date - rec.invoice_date_due).days ) # Due date to payment date
                    overdue_total -= payment.amount

            if overdue_total:
                overdue_interest += (overdue_total * rec.overdue_interest_rate / 100) * ( (fields.Date.today() - rec.invoice_date_due).days ) # Due date to today

            rec.overdue_interest_at_check_date = overdue_interest







