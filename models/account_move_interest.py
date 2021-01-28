from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInterest(models.Model):
    _name = 'account.interest'
    _description = 'Calculate overdue invoice interest'

    name = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    partner_ids = fields.Many2many('res.partner', string="Customers", required=True)
    create_date = fields.Date(string="Check Date", required=True, default=fields.Date.today)

    invoice_ids = fields.Many2many('account.move', string="Overdue invoices")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('account.interest.sequence') or _('New')

        result = super(AccountInterest, self).create(vals)
        return result

    def check_overdue_interest(self):
        """
        Loop All Chosen Partners, If Parter Has Overdue Invoice Then Modify Invoice And Add To The View
        """

        # Clear List Invoice In View
        self.invoice_ids = [(5 ,0 ,0)]

        for partner_id in self.partner_ids:
            print('------------------')
            print(partner_id.name)

            partner_invoices = self.env['account.move'].search([ ('partner_id', '=', partner_id.id), ('type', 'in', ('out_invoice', 'out_refund')) ])
            check_date = fields.Date.today()

            for invoice in partner_invoices:
                # Case due date and not paid all the money
                if invoice.invoice_date_due < fields.Date.today() and invoice.amount_residual > 0:
                    print('Overdue Invoice:',invoice)

                    vals = {
                        'overdue_check_date': check_date,
                    }

                    invoice.write(vals)

                    invoice.calculate_overdue_interest()

                    self.invoice_ids += invoice

                # Case paid all money but has payment due date
                if invoice.invoice_payment_state == 'paid':
                    payment_overdue = invoice.get_payments_overdue()
                    if len(payment_overdue) > 0:
                        print('Overdue Invoice:', invoice)

                        vals = {
                            'overdue_check_date': check_date,
                        }

                        invoice.write(vals)

                        invoice.calculate_overdue_interest()

                        self.invoice_ids += invoice

    def create_invoice(self):
        print('create_invoice')
        print(self.env['account.move'].browse(3).read())

        invoices = self.env['account.move'].browse(3).filtered(lambda move: move.has_overdue_interest == True)
        print(invoices)


