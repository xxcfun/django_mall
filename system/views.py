from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from mall.models import News
from utils import constants


def news_list(request, template_name='news_list.html'):
    """新闻列表"""
    news = News.objects.filter(types=constants.NEWS_TYPE_NEW,
                               is_valid=True)
    return render(request, template_name, {
        'news_list': news
    })


def news_detail(request, pk, template_name='news_info.html'):
    """新闻详情"""
    new_obj = get_object_or_404(News, pk=pk, is_valid=True)
    new_obj.view_count = F('view_count') + 1
    new_obj.save()
    return render(request, template_name, {
        'new_obj': new_obj
    })
