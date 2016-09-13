# coding=utf-8
import os
import datetime
import plistlib

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Case, When, Sum, IntegerField, Value

from django.conf import settings
from SportscarStyle.celery import app
from Club.models import ClubBillboard, Club


MAX_ORDER = 100

#
# @app.task()
# def update_billboard():
#     cities_path = os.path.abspath(
#         os.path.join(settings.BASE_DIR, "SportscarStyle", "data", "ChineseSubdivisions.plist")
#     )
#     cities = plistlib.readPlist(cities_path)
#
#     latest_billboard_obj = ClubBillboard.objects.order_by("-created_at").first()
#     if latest_billboard_obj is None:
#         next_billboard_version = 0
#     else:
#         next_billboard_version = latest_billboard_obj.version + 1
#
#     for provinces in cities.keys():
#         for city in provinces[0].keys():
#
#             def update_club_at_billboard(filter_type, new_list):
#                 for order, club in enumerate(new_list, 1):
#                     try:
#                         old_billboard = ClubBillboard.objects.get(
#                             club=club, version=next_billboard_version - 1, scope=city, filter_type=filter_type
#                         )
#                         old_order = old_billboard.order
#                         ClubBillboard.objects.create(
#                             club=club, order=order, d_order=order - old_order, scope=city, filter_type=filter_type,
#                             new_to_list=False
#                         )
#                     except ObjectDoesNotExist:
#                         ClubBillboard.objects.create(
#                             club=club, order=order, d_order=0, scope=city, filter_type=filter_type, new_to_list=True
#                         )
#
#             update_club_at_billboard(
#                 "total",
#                 Club.objects.filter(identified=True).order_by("-value_total")[0:MAX_ORDER]
#             )
#             update_club_at_billboard(
#                 'average',
#                 Club.objects.filter(identified=True).order_by('-value_average')[0:MAX_ORDER]
#             )
#             update_club_at_billboard(
#                 'members',
#                 Club.objects.annotate(members_num=Count("members")).order_by('-members_num')[0:MAX_ORDER]
#             )
#             update_club_at_billboard(
#                 'females',
#                 Club.objects.annotate(
#                     females=Sum(
#                         Case(When(members__gender='f', then=Value(1)),
#                              default=Value(0), output_field=IntegerField())
#                     )
#                 ).order_by('-females')[0:MAX_ORDER]
#             )
#             # # 总价排名
#             # filter_type = "total"
#             # best_total_values = Club.objects.filter(identified=True).order_by("-value_total")[0:MAX_ORDER]
#             # for order, club in enumerate(best_total_values, 1):
#             #     try:
#             #         old_billboard = ClubBillboard.objects.get(
#             #             club=club, version=next_billboard_version-1, scope=city, filter_type=filter_type
#             #         )
#             #         old_order = old_billboard.order
#             #         ClubBillboard.objects.create(
#             #             club=club, order=order, d_order=order - old_order, scope=city, filter_type=filter_type,
#             #             new_to_list=False
#             #         )
#             #     except ObjectDoesNotExist:
#             #         ClubBillboard.objects.create(
#             #             club=club, order=order, d_order=0, scope=city, filter_type=filter_type, new_to_list=True
#             #         )
#             # # 均价排名
#             # filter_type = "average"
#             # best_average_values = Club.objects.filter(identified=True).order_by('-value_average')[0:MAX_ORDER]
#             # for order, club in enumerate(best_average_values, 1):
#             #     try:
#             #         old_billboard = ClubBillboard.objects.get(
#             #             ClubBillboard.objects
#             #         )
#
#
# @app.task()
# def test():
#     print "haha"
