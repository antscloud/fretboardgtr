from typing import Any, Dict


class ConfigIniter:
    """Mixin class that define methods read the different configurations.

    All the components/elements configuration must subclass this Mixin.
    Then, all the configuration can be read thank to the method (eg
    from_dict) recursively
    """

    @classmethod
    def from_dict(cls, _dict: Dict) -> Any:
        kwargs = {}
        for arg, _type in cls.__annotations__.items():
            if arg not in _dict:
                continue
            if hasattr(_type, "from_dict"):
                kwargs[arg] = _type.from_dict(_dict[arg])
            else:
                kwargs[arg] = _dict[arg]
        return cls(**kwargs)
