# coding=utf-8
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.db.models import Q

from custom.utils import login_first
from .models import ChatRecordBasic
# Create your views here.


@require_GET
@login_first
def chat_list(request):
    """ 暂时先返回所有的聊天单元
     返回的信息包括每个单元的类型(private/group),目标信息(target_user/target_club),以及最近的一条聊天的内容
    """
    result = ChatRecordBasic.objects.select_related("sender__profile", "target_club")\
        .order_by("-created_at")\
        .filter(Q(target_user=request.user) | Q(target_club__members=request.user), deleted=False)\
        .distinct("distinct_identifier")

    return JsonResponse(dict(success=True, data=map(lambda x: x.dict_description(), result)))
