from typing import Any

import libcst
import libcst.matchers as m

from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand

_IO_OBJECTS = {
    "StringIO",
    "BytesIO",
}

# TODO import io automatically
class ConvertSixIO(VisitorBasedCodemodCommand):
    def leave_Attribute(
        self, original: libcst.Attribute, updated: libcst.Attribute
    ) -> Any:
        if m.matches(updated.value, m.Name("six")):
            if m.matches(updated.attr, m.Name()):
                if updated.attr.value in _IO_OBJECTS:
                    return libcst.Attribute(
                        value=libcst.Name("io"),
                        attr=updated.attr,
                    )
        return updated
