from peewee import *

from common.transformer import model_to_dict_wrapper
from common.util import extract_domain
from database.base_model import DynamicModel


class RSSEntryModel(DynamicModel):
    title = CharField()
    author = CharField(null=True)
    published_datetime = CharField()
    link = CharField(unique=True)
    summary = CharField()
    tags = CharField(null=True)
    media_thumbnail = CharField(null=True)
    show = BooleanField(default=True)

    class Meta:
        table_name = 'RSS_ENTRY'

    @staticmethod
    def get_not_dismissed_entries():
        query = RSSEntryModel.select()\
            .where(RSSEntryModel.show)\
            .limit(100)\
            .order_by(RSSEntryModel.published_datetime.asc())
        return [augment(model_to_dict_wrapper(item, keys=['datetime_created'])) for item in query]

    @staticmethod
    def dismiss(id_):
        query = RSSEntryModel.update(show=False).where(RSSEntryModel.id == id_)
        query.execute()


def augment(d):
    d['site'] = extract_domain(d['link'])
    d['tags'] = eval(d['tags'])
    return d


if __name__ == "__main__":
    RSSEntryModel.regenerate()
