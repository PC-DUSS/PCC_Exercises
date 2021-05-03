import typing


class Foo:
    method: str
    path: str
    headers: typing.Mapping[str, str]


foo = Foo()
print(vars(foo))
print(vars(Foo))
