import json

from odoo.tests import TransactionCase

from etv.core import EmployeeBag


class TestEtv(TransactionCase):

    def test_json_tree(self):
        etv = self.env['etv.etv']
        bag = etv.employees()
        jsn = json.loads(etv.to_json())
        self.assertIsInstance(bag, EmployeeBag)
        self.assertIsInstance(jsn, list)
