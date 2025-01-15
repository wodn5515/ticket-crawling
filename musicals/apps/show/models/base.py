from django.db import models


class ShowType(models.Model):
    name = models.CharField(max_length=50, verbose_name="공연분류")

    class Meta:
        db_table = "show_showtype"


class Show(models.Model):
    show_type = models.ForeignKey("show.ShowType", on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name="공연명")
    start_date = models.DateField(verbose_name="공연 시작일")
    end_date = models.DateField(verbose_name="공연 종료일")
    stadium = models.CharField(verbose_name="공연장소")

    class Meta:
        db_table = "show_show"
