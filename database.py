from datetime import datetime
import peewee as pw
from settings import RagatonSettings

config = RagatonSettings()

db = pw.PostgresqlDatabase(
    database="ragaton",
    user=config.postgres_user,
    password=config.postgres_password,
    host=config.postgres_host,
    port=config.postgres_port,
)


class NewsArticle(pw.Model):
    url = pw.CharField(unique=True)
    status = pw.IntegerField(default=200)
    created_at = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


class YoutubeVideo(pw.Model):
    url = pw.CharField(unique=True)
    status = pw.IntegerField(default=200)
    created_at = pw.DateTimeField(default=datetime.now)

    class Meta:
        database = db


with db:
    db.create_tables([NewsArticle, YoutubeVideo])
