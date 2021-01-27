from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInterest(models.Model):
    _name = 'account.interest'
    _description = 'Calculate overdue invoice interest'

    name = fields.Char(string="ID", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    partner_ids = fields.Many2many('res.partner', string="Customers", required=True)
    create_date = fields.Date(string="Date", required=True, default=fields.Date.today)

    invoice_ids = fields.Many2many('account.move', string="Overdue invoices")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('account.interest.sequence') or _('New')

        result = super(AccountInterest, self).create(vals)
        return result

    def check_overdue_interest(self):
        print('check_overdue_interest')
        print(self.partner_ids)

        self.invoice_ids = [(5 ,0 ,0)]

        for partner_id in self.partner_ids:
            print(partner_id)

            Overdue_invoices = self.env['account.move'].search([ ('has_overdue_interest', '=', True), ('partner_id', '=', partner_id.id), ('type', 'in', ('out_invoice', 'out_refund')) ])

            self.invoice_ids += Overdue_invoices
            # for invoice in Overdue_invoices:
            #     print(invoice)
            #     self.invoice_ids = invoice


    def create_invoice(self):
        print('create_invoice')
        print(self.env['account.move'].browse(3).read())

        invoices = self.env['account.move'].browse(3).filtered(lambda move: move.has_overdue_interest == True)
        print(invoices)


