# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

import re
import os

from odoo import tools
from odoo.modules import get_module_resource
from odoo.tools.config import config


file_store = config.filestore(dbname=config.get('db_name'))


def get_full_path(path):
    path = re.sub('[.]', '', path)
    path = path.strip('/\\')
    return os.path.join(file_store, path)


def get_image(image_path):
    content = open(get_full_path(image_path), 'rb').read().encode('base64')
    return tools.image_resize_image_big(content)


def get_default_image(mod_name='hr'):
    image_path = get_module_resource(
        mod_name,
        'static/src/img',
        'default_image.png'
    )
    content = open(image_path, 'rb').read().encode('base64')
    return tools.image_resize_image_big(content)

