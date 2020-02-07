import libcst
import libcst.matchers as m

from libcst.codemod import CodemodContext, VisitorBasedCodemodCommand


class RemoveUnicodeCompatible(VisitorBasedCodemodCommand):
    """
    Transform 

    ClassDef(
      name=Name(
        value='Foo',
      ),
      body=IndentedBlock(
        body=[
          SimpleStatementLine(
            body=[
              Pass(),
            ],
          ),
        ],
      ),
      decorators=[
        Decorator(
          decorator=Attribute(
            value=Name(
              value='six',
            ),
            attr=Name(
              value='python_2_unicode_compatible',
            ),
          ),
        ),
      ],
    )

    by removing any decorators that look like six.python_2_unicode_compatible.
    """

    def leave_ClassDef(
        self, original: libcst.ClassDef, updated: libcst.ClassDef
    ) -> libcst.ClassDef:
        resulting_decorators = []
        for decorator_wrapper in updated.decorators:
            decorator = decorator_wrapper.decorator
            if not m.matches(
                decorator,
                m.Attribute(
                    value=m.Name("six"), attr=m.Name("python_2_unicode_compatible"),
                ),
            ):
                resulting_decorators.append(decorator_wrapper)
        return updated.with_changes(decorators=resulting_decorators)
