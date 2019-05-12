class ObjectNotFoundInDBException(Exception):
    pass


class ObjectAlreadyExistsInCollectionException(Exception):
    pass


class ObjectNotFoundInCollectionException(Exception):
    pass


class ObjectExistsInDBException(Exception):
    object_id: int = None
