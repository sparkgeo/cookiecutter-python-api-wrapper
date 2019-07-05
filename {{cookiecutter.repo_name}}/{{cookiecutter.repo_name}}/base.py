
class Base:
    def __init__(self, client=None, **kwargs):
        self._client = client

    @classmethod
    def from_dict(cls, data_dict, client=None, **kwargs):
        pass
