from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.full_name]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id]
    column_default_sort = [(User.email, True), (User.full_name, False)]
    column_details_exclude_list = [User.hashed_password]

    # pagination configuration
    page_size = 50
    page_size_options = [25, 50, 100, 200]
