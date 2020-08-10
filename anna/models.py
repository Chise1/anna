from tortoise.models import Model
from tortoise import fields

from anna.contrib.auth.hashers import make_password


class abcModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class ModelAndTime(abcModel):
    created_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True


class Permission(ModelAndTime):
    code = fields.CharField(max_length=16, unique=True, description="权限码")
    description = fields.CharField(max_length=32, description="权限注释")
    model = fields.CharField(max_length=64, description="对应model", null=True)
    users: fields.ManyToManyRelation['User']
    groups: fields.ManyToManyRelation['Group']


class User(ModelAndTime):
    username = fields.CharField(max_length=32, description="用户名", unique=True)
    password = fields.CharField(max_length=32, description="密码")  # 用户密码拼接key之后MD5多重加密
    email = fields.CharField(max_length=32, description="邮箱", null=True)
    is_staff = fields.BooleanField(default=False, description="是否为职员")
    is_superuser = fields.BooleanField(default=False, description="是否为超级用户")
    is_del = fields.BooleanField(default=False, description="是否被删除")
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField("models.Permission",
                                                                                related_name="users")
    groups: fields.ManyToManyRelation['Group']

    def make_password(self, raw_password:str):
        """
        设置密码
        :param raw_password: 未加密的密码
        """
        return make_password(raw_password)


class Group(ModelAndTime):
    name = fields.CharField(max_length=32, description="组名")
    description = fields.CharField(max_length=255, description="组描述")
    users: fields.ManyToManyRelation['User'] = fields.ManyToManyField('models.User', related_name="groups")
    permissions: fields.ManyToManyRelation[Permission] = fields.ManyToManyField('models.Permission',
                                                                                related_name="groups")