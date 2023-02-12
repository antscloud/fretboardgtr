class ConfigIniter:
    @classmethod
    def from_dict(cls, _dict):
        kwargs = {}
        for arg, _type in cls.__annotations__.items():
            if arg not in _dict:
                continue
            if hasattr(_type, "from_dict"):
                kwargs[arg] = _type.from_dict(_dict[arg])
            else:
                kwargs[arg] = _dict[arg]
        return cls(**kwargs)
