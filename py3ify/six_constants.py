from typing import Any

import libcst
import libcst.matchers as m

from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand

_CONVERSION_MAP = {
    "class_types": libcst.Name("type"),
    "integer_types": libcst.Name("int"),
    "string_types": libcst.Name("str"),
    "text_type": libcst.Name("str"),
    "binary_type": libcst.Name("bytes"),
    "MAXSIZE": libcst.Attribute(value=libcst.Name("sys"), attr=libcst.Name("maxsize")),
}


class ConvertSixConstants(VisitorBasedCodemodCommand):
    def leave_Attribute(
        self, original: libcst.Attribute, updated: libcst.Attribute
    ) -> Any:
        if m.matches(updated.value, m.Name("six")):
            if m.matches(updated.attr, m.Name()):
                return _CONVERSION_MAP.get(updated.attr.value, updated)
        return updated
