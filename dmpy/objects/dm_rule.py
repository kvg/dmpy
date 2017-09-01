import attr


def convert_to_list(val):
    if val is None:
        return []
    if isinstance(val, str):
        return [val]
    else:
        return list(val)


@attr.s(slots=True)
class DMRule(object):
    target = attr.ib()
    deps = attr.ib(attr.Factory(list), convert=convert_to_list)
    recipe = attr.ib(attr.Factory(list), convert=convert_to_list)
