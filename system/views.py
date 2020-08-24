from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render, get_object_or_404

# Create your views here.
from system.models import News
from utils import constants
from utils.verify import VerifyCode


def news_list(request, template_name='news_list.html'):
    """新闻列表"""
    # 当前页码
    page = request.GET.get('page', 1)
    page_size = 20  # 每页放20条数据

    news = News.objects.filter(types=constants.NEWS_TYPE_NEW,
                               is_valid=True)
    paginator = Paginator(news, page_size)
    page_data = paginator.page(page)
    return render(request, template_name, {
        'page_data': page_data
    })


def news_detail(request, pk, template_name='news_info.html'):
    """新闻详情"""
    new_obj = get_object_or_404(News, pk=pk, is_valid=True)
    new_obj.view_count = F('view_count') + 1
    new_obj.save()
    # 重新从数据库取数据
    new_obj.refresh_from_db()
    return render(request, template_name, {
        'new_obj': new_obj
    })


def verify_code(request):
    client = VerifyCode(request)
    return client.gen_code()
