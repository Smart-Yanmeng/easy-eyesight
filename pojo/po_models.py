from datetime import datetime

from tortoise import Model
from tortoise import fields


class User(Model):
    user_id = fields.BigIntField(pk=True, description="用户ID")
    org = fields.ForeignKeyField("models.Org", related_name="users")
    username = fields.CharField(max_length=16, description="用户名")
    face_img = fields.BinaryField(description="照片")
    create_time = fields.DatetimeField(default=datetime.utcnow(), description="创建时间")


class Org(Model):
    org_id = fields.BigIntField(pk=True, description="机构ID")
    org_name = fields.CharField(max_length=64, description="机构名")
    org_type = fields.IntField(description="机构类型")
