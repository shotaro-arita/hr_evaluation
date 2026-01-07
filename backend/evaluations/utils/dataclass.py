import copy
from dataclasses import fields
from typing import Any, Callable


def _is_dataclass_instance(obj: Any) -> bool:
    """Returns True if obj is an instance of a dataclass."""
    _FIELDS = "__dataclass_fields__"
    return hasattr(type(obj), _FIELDS)


def asdict(
    obj: Any, *, dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict
) -> dict[str, Any]:
    """
    = field(metadata={"dump_skip": True})
    出力するdictのキー名を変えたい時は、{"output_name":出力したい名前}
    """

    if not _is_dataclass_instance(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_inner(obj, dict_factory)


def _asdict_inner(
    obj: Any, dict_factory: Callable[[list[tuple[str, Any]]], dict[str, Any]] = dict
) -> Any:
    if _is_dataclass_instance(obj):
        result = []
        for f in fields(obj):
            # added
            if f.metadata.get("dump_skip", False):
                continue

            value = _asdict_inner(getattr(obj, f.name), dict_factory)

            # 出力名(output_name)が設定されている場合は、dictのkey名を変更
            key = f.metadata.get("output_name", f.name)

            result.append((key, value))
        return dict_factory(result)
    elif isinstance(obj, tuple) and hasattr(obj, "_fields"):
        return type(obj)(*[_asdict_inner(v, dict_factory) for v in obj])
    elif isinstance(obj, (list, tuple)):
        return type(obj)(_asdict_inner(v, dict_factory) for v in obj)
    elif isinstance(obj, dict):
        return type(obj)(
            (_asdict_inner(k, dict_factory), _asdict_inner(v, dict_factory))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)
