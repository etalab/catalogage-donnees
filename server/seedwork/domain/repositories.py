import itertools

IDS = itertools.count(0)


class Repository:
    @staticmethod
    def make_id() -> int:
        return next(IDS)
