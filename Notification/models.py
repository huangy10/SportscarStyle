# coding=utf-8
from django.db import models
from django.conf import settings
# Create your models here.


class Notification(models.Model):

    target = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="目标用户")
    message_type = models.CharField(max_length=100, choices=(
        ("status_like", "status_like"),
        ("status_comment", "your_status_are_commmented_by_others"),
        ("status_comment_replied", "your_comment_on_a_status_is_responsed_by_others"),
        ("news_comment_replied", "your commemnt_on_a_news_is_responsed_by_others"),
        ("act_applied", "some_one_applys_your_activity"),
        ("act_approved", "your_application_on_an_activity_is_approved"),
        ("act_denied", "your_application_on_an_activity_is_denied"),
        ("act_full", "one_of_your_activity_if_full_off_applicators"),
        ("act_deleted", "one_of_your_applied_activity_is_deleted"),
        ("act_application_cancel", "one_application_is_cancelled"),
        ("act_invited", "some_one_invite_you_for_an_activity"),
        ("act_invitation_agreed", "your_invitation_is_agreed"),
        ("act_invitation_denied", "your_invitation_is_denied"),
        ("auth_car_approved", "your_application_for_sportscar_identification_is_approved"),
        ("auth_car_denied", "your_application_for_sportscar_identification_is_denied"),
        ("auth_club_approved", "your_application_for_club_identification_is_approved"),
        ("auth_club_denied", "your_application_for_club_identification_is_denied"),
        ("auth_act_approved", ""),
        ("auth_act_denied", ""),
        ("relation_follow", ""),
    ))
    related_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    related_act = models.ForeignKey("Activity.Activity", related_name="+")
    related_club = models.ForeignKey("Club.Club", related_name="+")
    related_status = models.ForeignKey("Status.Status", related_name="+")
    related_status_comment = models.ForeignKey("Status.StatusComment", related_name="+")
    related_news = models.ForeignKey("News.News", related_name="+")
    related_news_comment = models.ForeignKey("News.NewsComment", related_name="+")

    message_body = models.CharField(max_length=255, verbose_name="消息内容(Optional)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
         ordering = ("-created_at", )
         verbose_name = "消息"
         verbose_name_plural = "消息"

    def dict_description(self):
        """ 获取字典表示形式
        """
        return dict()
