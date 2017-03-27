# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
)

from odoo import models, api

from etv.core import (
    EmployeeRec,
    EmployeeBag,
)


class Etv(models.Model):

    _inherit = 'hr.employee'

    @api.model
    def employees(self, **kwargs):
        recs = EmployeeRec.build_tree(cursor=self._cr, **kwargs)
        return EmployeeBag(recs)

    @api.model
    def to_json(self, indent=None, **kwargs):
        recs = EmployeeRec.build_tree(cursor=self._cr, **kwargs)
        return EmployeeBag(recs).to_json(indent=indent)
