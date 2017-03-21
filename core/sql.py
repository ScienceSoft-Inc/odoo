# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from odoo.api import Environment
from odoo.modules.registry import RegistryManager
from odoo.tools.config import config


EMPLOYEES_QUERY = """
    WITH RECURSIVE employees(
            id,
            parent_id,
            name,
            work_phone,
            mobile_phone,
            email,
            image,
            gender,
            group_id,
            depth
        ) AS (
        SELECT t.id,
               parent_id,
               name_related as name,
               work_phone,
               mobile_phone,
               work_email as email,
               a.store_fname as image,
               gender,
               t.id AS group_id,
               0 AS depth
          FROM hr_employee as t
          LEFT OUTER JOIN ir_attachment as a
            ON (a.res_id = t.id AND
                a.res_model = 'hr.employee' AND
                a.res_field = 'image')
          WHERE parent_id is NULL
        UNION ALL
        SELECT t.id,
               t.parent_id,
               t.name_related as name,
               t.work_phone,
               t.mobile_phone,
               t.work_email as email,
               a.store_fname as image,
               t.gender,
               e.group_id,
               e.depth + 1
            FROM hr_employee AS t
            LEFT OUTER JOIN ir_attachment as a
            ON (a.res_id = t.id AND
                a.res_model = 'hr.employee' AND
                a.res_field = 'image')
            JOIN employees AS e ON
            (e.id = t.parent_id)
    )
    SELECT * FROM employees
"""


def connect(uid=1, context=None):
    reg = RegistryManager.get(config.get('db_name'))
    cr = reg.cursor()
    Environment.reset()
    env = Environment(cr, uid, context or {})
    return env


def get_employee_records():
    env = connect(config.get('db_name'))
    cursor = env.cr
    cursor.execute(EMPLOYEES_QUERY)
    while True:
        try:
            rec = cursor.next()
            yield rec
        except StopIteration:
            break
    cursor.close()
    Environment.reset()
