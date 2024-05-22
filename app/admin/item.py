from sqladmin import ModelView

from app.models import Item


class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.title, Item.description]
    column_searchable_list = [Item.title]
    column_sortable_list = [Item.id]
    column_details_exclude_list = [Item.owner]

    # pagination configuration
    page_size = 50
    page_size_options = [25, 50, 100, 200]
