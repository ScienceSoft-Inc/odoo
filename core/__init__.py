# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
)
import json
from collections import namedtuple
from operator import attrgetter

from .attachment import (
    get_image,
    get_default_image,
)
from .sql import get_employee_records
from .serialize import BufferJsonEncoder


class EmployeeRec(namedtuple('Employee', [
    'id',
    'parent_id',
    'name',
    'work_phone',
    'mobile_phone',
    'email',
    'image',
    'gender',
    'department',
    'group_id',
    'depth',
    'children'
])):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super(EmployeeRec, self).__init__(*args, **kwargs)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.id, self.parent_id or 0, self.name)

    def __hash__(self):
        return self.id

    @classmethod
    def fetch(cls, **kwargs):
        for rec in get_employee_records(**kwargs):
            yield cls.create(*rec)

    @classmethod
    def create(cls, *args):
        rec = cls(*(args + ([],)))
        img = (get_image(rec.image) if rec.image is not None
               else get_default_image())
        return rec._replace(image=img)

    @classmethod
    def build_tree(cls, **kwargs):
        flt = set()
        storage = {}
        for rec in cls.fetch(**kwargs):
            storage[rec.id] = rec
        for rec in storage.itervalues():
            if rec.parent_id is not None:
                storage[rec.parent_id].children.append(rec)
                flt.add(rec.id)
        for key in flt:
            storage.pop(key)
        return storage.itervalues()

    def traverse(self):
        yield self
        for item in (_ for child in self.children for _ in child.traverse()):
            yield item

    def to_json(self):
        return json.dumps(self.as_dict(), cls=BufferJsonEncoder)

    def as_dict(self):
        dct = self._asdict()
        dct['children'] = [child.as_dict() for child in dct['children']]
        return dct


class EmployeeBag(object):

    def __init__(self, values):
        self.values = sorted(values, key=attrgetter('id'))

    def __str__(self):
        gen = ('{}{}'.format(' ' * item.depth * 4, item) for item in self.tree)
        return '\n'.join(gen).encode('utf8')

    @property
    def tree(self):
        for value in self.values:
            for item in value.traverse():
                yield item

    def __iter__(self):
        return self.tree

    def to_json(self, indent=None):
        return json.dumps(
            [value.as_dict() for value in self.values], indent=indent, cls=BufferJsonEncoder)
