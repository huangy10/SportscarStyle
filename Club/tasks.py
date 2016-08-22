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


@app.task()
def update_billboard():
    cities_path = os.path.abspath(
        os.path.join(settings.BASE_DIR, "SportscarStyle", "data", "ChineseSubdivisions.plist")
    )
    cities = plistlib.readPlist(cities_path)

    latest_billboard_obj = ClubBillboard.objects.order_by("-created_at").first()
    if latest_billboard_obj is None:
        next_billboard_version = 0
    else:
        next_billboard_version = latest_billboard_obj.version + 1

    def update_club_at_billboard(filter_type, new_list, scope):
        for order, club in enumerate(new_list, 1):
            try:
                old_billboard = ClubBillboard.objects.get(
                    club=club, version=next_billboard_version - 1, scope=scope, filter_type=filter_type
                )
                old_order = old_billboard.order
                ClubBillboard.objects.create(
                    club=club, order=order, d_order=order - old_order, scope=scope, filter_type=filter_type,
                    new_to_list=False, version=next_billboard_version
                )
            except ObjectDoesNotExist:
                ClubBillboard.objects.create(
                    club=club, order=order, d_order=0, scope=scope, filter_type=filter_type, new_to_list=True,
                    version=next_billboard_version
                )

    for (_, prov) in cities.items():
        for city in prov[0].keys():
            update_club_at_billboard(
                "total",
                Club.objects.filter(identified=True, city=city).order_by("-value_total")[0:MAX_ORDER],
                city
            )
            update_club_at_billboard(
                'average',
                Club.objects.filter(identified=True, city=city).order_by('-value_average')[0:MAX_ORDER],
                city
            )
            update_club_at_billboard(
                'members',
                Club.objects.filter(identified=True, city=city)
                    .annotate(members_num=Count("members")).order_by('-members_num')[0:MAX_ORDER],
                city
            )
            update_club_at_billboard(
                'females',
                Club.objects.filter(identified=True, city=city).annotate(
                    females=Sum(
                        Case(When(members__gender='f', then=Value(1)),
                             default=Value(0), output_field=IntegerField())
                    )
                ).order_by('-females')[0:MAX_ORDER],
                city
            )
    city = u'全国'
    update_club_at_billboard(
        "total",
        Club.objects.filter(identified=True).order_by("-value_total")[0:MAX_ORDER],
        city
    )
    update_club_at_billboard(
        'average',
        Club.objects.filter(identified=True).order_by('-value_average')[0:MAX_ORDER],
        city
    )
    update_club_at_billboard(
        'members',
        Club.objects.filter(identified=True)
            .annotate(members_num=Count("members")).order_by('-members_num')[0:MAX_ORDER],
        city
    )
    update_club_at_billboard(
        'females',
        Club.objects.filter(identified=True).annotate(
            females=Sum(
                Case(When(members__gender='f', then=Value(1)),
                     default=Value(0), output_field=IntegerField())
            )
        ).order_by('-females')[0:MAX_ORDER],
        city
    )


@app.task()
def club_value_change(club):
    club.recalculate_value(commit=True)
