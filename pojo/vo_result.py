class R(object):
    """
    统一返回类
    """
    code: int
    msg: str
    data: object

    def __init__(self, code: int, msg: str, data: object):
        self.code = code
        self.msg = msg
        self.data = data

    def __repr__(self):
        return f'R(code={self.code}, msg={self.msg}, data={self.data})'

    @staticmethod
    def ok(code=200, msg='ok', data=None):
        return R(code, msg, data)

    @staticmethod
    def error(code=400, msg='error', data=None):
        return R(code, msg, data)
