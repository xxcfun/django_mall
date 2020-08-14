from django.shortcuts import render

# Create your views here.


def templ_filter_mine(request):
    list = ('北京', '上海', '广州', '山东')
    return render(request, 'templ_filter_mine.html', {
        'list': list
    })