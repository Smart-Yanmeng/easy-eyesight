class MultiFaceError(Exception):
    def __init__(self):
        self.message = "Too many faces found !"
        super().__init__(self.message)


class NoFaceError(Exception):
    def __init__(self):
        self.message = "No face found !"
        super().__init__(self.message)
