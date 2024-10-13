class ServiceMessage:
    success: bool
    data: dict
    error: dict

    def __init__(self, success: bool = True, data : dict = {}, error : dict = {}):
        self.success = success
        self.data = data
        self.error = error