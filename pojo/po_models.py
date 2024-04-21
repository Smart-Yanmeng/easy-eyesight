from datetime import datetime

from tortoise import Model
from tortoise import fields


class User(Model):
    """
    :keyword 用户表
    """
    user_id = fields.BigIntField(pk=True, description="用户ID")
    org = fields.ForeignKeyField("models.Org", related_name="users")
    username = fields.CharField(max_length=16, description="用户名")
    face_img = fields.BinaryField(description="照片")
    create_time = fields.DatetimeField(default=datetime.utcnow(), description="创建时间")


class Org(Model):
    """
    :keyword 组织表
    """
    org_id = fields.BigIntField(pk=True, description="机构ID")
    org_name = fields.CharField(max_length=64, description="机构名")
    org_type = fields.IntField(description="机构类型")


class Record(Model):
    """
    :keyword 记录表
    """
    record_id = fields.BigIntField(pk=True, description="记录ID")
    user = fields.ForeignKeyField("models.User", related_name="records")
    left_with_glasses = fields.FloatField(description="左眼矫正视力")
    right_with_glasses = fields.FloatField(description="右眼矫正视力")
    left_naked_eye = fields.FloatField(description="左眼裸眼视力")
    right_naked_eye = fields.FloatField(description="右眼裸眼视力")
    create_time = fields.DatetimeField(default=datetime.utcnow(), description="创建时间")
