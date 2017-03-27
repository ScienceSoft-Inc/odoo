# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from odoo import http
from odoo.http import Response


class EtvController(http.Controller):

    @http.route('/etv/tree/', auth='user', methods=['GET'], website='True')
    def index(self, **kw):
        etv = http.request.env['etv.etv']
        return Response(
            etv.to_json(indent=4),
            content_type='application/json; charset=utf-8'
        )


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
