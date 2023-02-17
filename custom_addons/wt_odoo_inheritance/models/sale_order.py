from odoo import api, models, fields, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
