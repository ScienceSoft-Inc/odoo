# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)

from openerp import tools
from openerp.modules import get_module_resource
from openerp.tools.config import config


file_store = config.filestore(dbname=config.get('db_name'))


def get_default_image(mod_name='hr'):
    image_path = get_module_resource(
        mod_name,
        'static/src/img',
        'default_image.png'
    )
    content = open(image_path, 'rb').read().encode('base64')
    return tools.image_resize_image_big(content)

