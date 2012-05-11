class AdminLockingBaseException(Exception):
        def __init__(self, obj, *args, **kwargs):
            self.obj = obj

class ObjectChangedException(AdminLockingBaseException):
    pass
        
class LockExistsException(AdminLockingBaseException):       
    pass