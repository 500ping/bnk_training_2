from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import json

class AccountInterest(models.Model):
    _name = 'account.interest'
    _description = 'Calculate overdue invoice interest'

    name = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    partner_ids = fields.Many2many('res.partner', string="Customers", required=True)
    create_date = fields.Date(string="Create Date", required=True, default=fields.Date.today)

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
        self.invoice_ids = [(5, 0, 0)]

        for partner_id in self.partner_ids:
            print('------------------')
            print(partner_id.name)

            partner_invoices = self.env['account.move'].search([ ('partner_id', '=', partner_id.id), ('type', 'in', ('out_invoice', 'out_refund')), ('is_overdue_invoice', '=', False) ])
            check_date = fields.Date.today()

            vals = {
                'overdue_check_date': check_date,
            }

            for invoice in partner_invoices:
                # Case due date and not paid all the money
                if invoice.invoice_date_due < fields.Date.today() and invoice.amount_residual > 0:
                    print('Overdue Invoice:',invoice)
                    invoice.write(vals)

                    self.invoice_ids += invoice

                # Case paid all money but has payment due date
                if invoice.invoice_payment_state == 'paid':
                    payment_overdue = invoice.get_payments_overdue()
                    if len(payment_overdue) > 0:
                        print('Overdue Invoice:', invoice)
                        invoice.write(vals)

                        self.invoice_ids += invoice

    def create_invoice(self):
        """
        Create Invoices From Overdue Invoice, If Partner Overdue Invoice Exists -> Set To Draft And Edit(Need To Re Add Payment)
        """
        if fields.Date.today() != self.create_date:
            self.check_overdue_interest()

        if not self.invoice_ids:
            raise ValidationError("Lam Deo Co Gi Ma Tao")

        for partner in self.partner_ids:

            # Get all invoice in view by partner
            invoices = self.invoice_ids.filtered(lambda invoice: invoice.partner_id == partner)
            if not invoices:
                break

            invoice_lines = []
            for invoice in invoices:
                description = invoice.calculate_overdue_interest()
                invoice_line = (0, 0, {
                    'name': description,
                    'price_unit': invoice.overdue_interest_at_check_date,
                })

                invoice_lines.append(invoice_line)

            overdue_invoice = self.env['account.move'].search([ ('partner_id' , '=', partner.id), ('is_overdue_invoice', '=', True) ])
            print( overdue_invoice )

            # Create Or Edit Overdue Invoice For Each Partner
            if overdue_invoice:
                # Roll Back To Draft
                overdue_invoice.button_draft()

                overdue_invoice.invoice_line_ids = [(5, 0, 0)]
                overdue_invoice.write({
                    'invoice_payment_ref': _(f'Overdue invoice - {partner.name}'),
                    'invoice_line_ids': invoice_lines,
                })
                overdue_invoice.action_post()
            else:
                self.env['account.move'].with_context(default_type='out_invoice').create({
                    'invoice_payment_ref': _(f'Overdue invoice - {partner.name}'),
                    'is_overdue_invoice': True,
                    'partner_id': partner.id,
                    'invoice_line_ids': invoice_lines,
                }).action_post()








