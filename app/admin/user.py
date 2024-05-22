from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
