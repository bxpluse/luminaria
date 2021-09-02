import json

from peewee import *

from common.transformer import model_to_dict_wrapper
from common.util import extract_domain
from database.base_model import DynamicModel


class FeedEntryModel(DynamicModel):
    title = CharField()
    author = CharField(null=True)
    published_datetime = CharField()
    link = CharField(unique=True)
    summary = CharField()
    tags = CharField(null=True)
    media_thumbnail = CharField(null=True)
    type = CharField()
    metadata = CharField()
    show = BooleanField(default=True)

    class Meta:
        table_name = 'FEED_ENTRY'

    @staticmethod
    def get_not_dismissed_entries():
        query = FeedEntryModel.select() \
            .where(FeedEntryModel.show) \
            .limit(100) \
            .order_by(FeedEntryModel.published_datetime.asc())
        return [augment(model_to_dict_wrapper(item)) for item in query]

    @staticmethod
    def dismiss(id_):
        query = FeedEntryModel.update(show=False).where(FeedEntryModel.id == id_)
        query.execute()


def augment(d):
    if d['type'] == 'SUBREDDIT':
        link = json.loads(d['metadata'])['url']
        d['site'] = extract_domain(link)
    else:
        d['site'] = extract_domain(d['link'])
    d['tags'] = eval(d['tags'])
    return d


if __name__ == "__main__":
    FeedEntryModel.regenerate()
