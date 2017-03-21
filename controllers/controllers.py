# -*- coding: utf-8 -*-
from odoo import http

# class Etv(http.Controller):
#     @http.route('/etv/etv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/etv/etv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('etv.listing', {
#             'root': '/etv/etv',
#             'objects': http.request.env['etv.etv'].search([]),
#         })

#     @http.route('/etv/etv/objects/<model("etv.etv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('etv.object', {
#             'object': obj
#         })