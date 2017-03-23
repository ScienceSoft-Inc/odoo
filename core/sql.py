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
            department,
            group_id,
            depth
        ) AS (
        SELECT t.id,
               t.parent_id,
               t.name_related AS name,
               t.work_phone,
               t.mobile_phone,
               t.work_email AS email,
               a.store_fname as image,
               t.gender,
               d.name AS department,
               t.id AS group_id,
               0 AS depth
          FROM hr_employee AS t
          LEFT OUTER JOIN hr_department AS d
          ON (t.department_id = d.id)
          LEFT OUTER JOIN ir_attachment as a
            ON (a.res_id = t.id AND
                a.res_model = 'hr.employee' AND
                a.res_field = 'image')
          WHERE t.parent_id is NULL
          {where:s}
        UNION ALL
        SELECT t.id,
               t.parent_id,
               t.name_related AS name,
               t.work_phone,
               t.mobile_phone,
               t.work_email AS email,
               a.store_fname as image,
               t.gender,
               d.name AS department,
               e.group_id,
               e.depth + 1
            FROM hr_employee AS t
            LEFT OUTER JOIN hr_department AS d
            ON (t.department_id = d.id)
            LEFT OUTER JOIN ir_attachment as a
            ON (a.res_id = t.id AND
                a.res_model = 'hr.employee' AND
                a.res_field = 'image')
            JOIN employees AS e
            ON (e.id = t.parent_id)
    )
    SELECT * FROM employees
"""


def connect(uid=1, context=None):
    reg = RegistryManager.get(config.get('db_name'))
    cr = reg.cursor()
    Environment.reset()
    env = Environment(cr, uid, context or {})
    return env


def get_employee_records(cursor=None, _id=None, department_id=None):
    flt = []
    params = []
    if department_id is not None:
        flt.append('AND d.department_id = %s')
        params.append(department_id)
    if _id is not None:
        flt.append('AND t.id = %s')
        params.append(_id)
    if cursor is None:
        env = connect(config.get('db_name'))
        cursor = env.cr
    query = EMPLOYEES_QUERY.format(where=' '.join(flt))
    cursor.execute(query, *params)
    while True:
        try:
            rec = cursor.next()
            yield rec
        except StopIteration:
            break
    if cursor is None:
        cursor.close()
        Environment.reset()
