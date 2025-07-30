from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate(request, queryset, per_page=10, order="id"):
    page = request.GET.get('page', 1)
    queryset = queryset.order_by(order)
    paginator = Paginator(queryset, per_page)

    try:
        paginated = paginator.page(page)
    except PageNotAnInteger:
        paginated = paginator.page(1)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    return paginated