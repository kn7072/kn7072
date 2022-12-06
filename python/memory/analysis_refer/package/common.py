# -*- coding: utf-8 -*-
import weakref
from typing import Any


class Meta(type):

    dict_ref = {}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        instance = super().__call__(*args, **kwds)
        path_to_instance = f"{instance.__module__}.{instance.__class__.__name__}"
        ref = weakref.ref(instance)

        if self.dict_ref.get(path_to_instance):
            self.dict_ref[path_to_instance].append(ref)
        else:
            self.dict_ref[path_to_instance] = []
            self.dict_ref[path_to_instance].append(ref)

        return instance
