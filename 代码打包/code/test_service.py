import warnings
import numpy as np
import aface
from peewee import *
import datetime

from face_service import *
# 忽略警告信息
warnings.filterwarnings("ignore", category=DeprecationWarning) 

db = SqliteDatabase('faces.db')


class TestModel(Model):
    
    face = ForeignKeyField(FaceModel, related_name='tests')

    test_data = TextField()

    test_time = DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db


class Test_service:
    def __init__(self):
        db.create_tables([TestModel])

    def get_tests_by_face(self, face_id):
        tests = [test.__dict__['__data__']  for test in TestModel.select().where(TestModel.face_id == face_id)]
        for i in tests:
            i['test_time'] = i['test_time'].strftime('%Y-%m-%d %H:%M:%S')
        return tests

    def delete_test_by_id(self, id):
        TestModel.get_by_id(id).delete_instance()

    def add_test(self, face_id, test_data):
        try:
            face = FaceModel.get(id=face_id)
            test = TestModel.create(test_data=test_data, face=face)
            return test.id
        except Exception as e:
            print(e)
            return False



if __name__ == "__main__":
    face_id = 1 # 假设为在faces表中 id 为1的记录
    test_service = Test_service()

    test_service.add_test(face_id,{"naked":{"right":"10",""},"correct":{}})

    tests = test_service.get_tests_by_face(face_id)

    for test in tests:
        print(test)