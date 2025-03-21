from django.db import models
from apps.common.models import TimeStampedModel


class TicketOpen(TimeStampedModel):
    show = models.ForeignKey("show.Show", on_delete=models.PROTECT, null=True)
    open_at = models.DateTimeField(verbose_name="오픈일시", null=True)
    has_detail_open_at = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    link = models.URLField()
    thumbnail = models.URLField(null=True)
    site = models.CharField(max_length=255)
    is_published = models.BooleanField(default=True)

    class Meta:
        db_table = "show_ticketopen"
        constraints = [
            models.UniqueConstraint(fields=["name", "site"], name="site_name_unique")
        ]
