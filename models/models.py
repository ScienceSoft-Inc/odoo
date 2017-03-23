# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
)

from openerp import models, api

from etv.core import (
    EmployeeRec,
    EmployeeBag,
)


class Etv(models.Model):

    _name = 'etv.etv'

    @api.model
    def employees(self):
        return EmployeeBag(EmployeeRec.build_tree())

    @api.model
    def to_json(self, indent=None):
        return EmployeeBag(EmployeeRec.build_tree()).to_json(indent=indent)
