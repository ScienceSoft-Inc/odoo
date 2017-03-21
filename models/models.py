# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)
from odoo import models, api

from etv.core import (
    EmployeeRec,
    EmployeeBag,
)


class Etv(models.Model):

    _inherit = 'hr.employee'

    @api.model
    def hr_tree(self):
        return EmployeeBag(EmployeeRec.build_tree())
