import libcst
import libcst.matchers as m

from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand

_CONVERSION_MAP = {
    "iteritems": "items",
    "iterkeys": "keys",
    "itervalues": "values",
    "viewitems": "items",
    "viewkeys": "keys",
    "viewvalues": "values",
}

class ConvertSixCollections(VisitorBasedCodemodCommand):
    """
    Transform 

    Call(
      func=Attribute(
        value=Name(value='six'),
        attr=Name(value='iteritems')
      ),
      args=[Arg(value=ARGUMENT]
    )

    to

    Call(
      func=Attribute(value=ARGUMENT, attr=Name(value='items')
    )
    """
    def leave_Call(self, original: libcst.Call, updated: libcst.Call) -> libcst.Call:
        if m.matches(updated.func.value, m.Name("six")):
            for orig_name, updated_name in _CONVERSION_MAP.items():
                if m.matches(updated.func.attr, m.Name(orig_name)):
                    assert len(updated.args) == 1
                    value = updated.args[0].value
                    return libcst.Call(func=libcst.Attribute(
                        value=value,
                        attr=libcst.Name(value=updated_name),
                    ))
        return updated
