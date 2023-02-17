# -*- coding: utf-8 -*-
# from odoo import http


# class WtOdooInheritance(http.Controller):
#     @http.route('/wt_odoo_inheritance/wt_odoo_inheritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wt_odoo_inheritance/wt_odoo_inheritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wt_odoo_inheritance.listing', {
#             'root': '/wt_odoo_inheritance/wt_odoo_inheritance',
#             'objects': http.request.env['wt_odoo_inheritance.wt_odoo_inheritance'].search([]),
#         })

#     @http.route('/wt_odoo_inheritance/wt_odoo_inheritance/objects/<model("wt_odoo_inheritance.wt_odoo_inheritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wt_odoo_inheritance.object', {
#             'object': obj
#         })
