# -*- coding: utf-8 -*-
# from odoo import http


# class DmInterestCalculation(http.Controller):
#     @http.route('/dm_interest_calculation/dm_interest_calculation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dm_interest_calculation/dm_interest_calculation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dm_interest_calculation.listing', {
#             'root': '/dm_interest_calculation/dm_interest_calculation',
#             'objects': http.request.env['dm_interest_calculation.dm_interest_calculation'].search([]),
#         })

#     @http.route('/dm_interest_calculation/dm_interest_calculation/objects/<model("dm_interest_calculation.dm_interest_calculation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dm_interest_calculation.object', {
#             'object': obj
#         })
