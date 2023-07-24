import logging
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
        for arg in _dict:
            if arg not in cls.__annotations__.keys():
                logging.warning(
                    f'"{arg}" key confuration was not found in {cls.__name__}'
                )
                continue
            _type = cls.__annotations__[arg]
            if hasattr(_type, "from_dict"):
                kwargs[arg] = _type.from_dict(_dict[arg])
            else:
                kwargs[arg] = _dict[arg]
        return cls(**kwargs)
