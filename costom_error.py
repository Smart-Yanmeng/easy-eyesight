class MultiFaceError(Exception):
    def __init__(self):
        self.message = "Too many faces found !"
        super().__init__(self.message)


class NoFaceError(Exception):
    def __init__(self):
        self.message = "No face found !"
        super().__init__(self.message)


class NoGlassesError(Exception):
    def __init__(self):
        self.message = "Please wear glasses !"
        super().__init__(self.message)


class HasGlassesError(Exception):
    def __init__(self):
        self.message = "Please take off glasses !"
        super().__init__(self.message)


class MatchFaceError(Exception):
    def __init__(self):
        self.message = "No match face found !"
        super().__init__(self.message)
