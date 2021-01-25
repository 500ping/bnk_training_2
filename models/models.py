# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class dm_interest_calculation(models.Model):
#     _name = 'dm_interest_calculation.dm_interest_calculation'
#     _description = 'dm_interest_calculation.dm_interest_calculation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
