from .StructFormatter import StructFormatter
from .StructNamedFormatter import StructNamedFormatter


def struct_format():
    """

    :rtype: StructFormatter
    """
    return StructFormatter()


def struct_named_format(struct_name):
    """

    :type struct_name: str
    :rtype: StructNamedFormatter
    """
    return StructNamedFormatter(struct_name)
