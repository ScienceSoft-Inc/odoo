# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from openerp.api import Environment
from openerp.modules.registry import RegistryManager
from openerp.tools.config import config


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
               t.image,
               t.gender,
               d.name AS department,
               t.id AS group_id,
               0 AS depth
          FROM hr_employee AS t
          LEFT OUTER JOIN hr_department AS d
          ON (t.department_id = d.id)
          WHERE t.parent_id is NULL
        UNION ALL
        SELECT t.id,
               t.parent_id,
               t.name_related AS name,
               t.work_phone,
               t.mobile_phone,
               t.work_email AS email,
               t.image as image,
               t.gender,
               d.name AS department,
               e.group_id,
               e.depth + 1
            FROM hr_employee AS t
            LEFT OUTER JOIN hr_department AS d
            ON (t.department_id = d.id)
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
