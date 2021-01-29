from odoo import api, fields, models, _

class CustomSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overdue_interest_rate = fields.Integer(string="interest")

    def set_values(self):
        res = super(CustomSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('account_move.overdue_interest_rate', self.overdue_interest_rate)
        return res

    @api.model
    def get_values(self):
        res = super(CustomSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        overdue_interest_rate = ICPSudo.get_param('account_move.overdue_interest_rate')
        res.update(
            overdue_interest_rate=int(overdue_interest_rate),
        )
        return res
