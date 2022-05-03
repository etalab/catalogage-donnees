from ..common.exceptions import DoesNotExist


class TagDoesNotExist(DoesNotExist):
    entity_name = "Tag"
