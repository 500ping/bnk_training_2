from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AccountInterestDetails(models.Model):
    _name = 'account.interest.details'
    _description = 'Details for overdue invoice'

    invoice_ids = fields.Many2one('account.move', string="Invoices")
