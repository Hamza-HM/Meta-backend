from rest_framework import filters

class CustomSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_value = request.query_params.get(self.search_param, '')
        if search_value.lower() == 'pending':
            return queryset.filter(status=0)
        elif search_value.lower() == 'delivered':
            return queryset.filter(status=1)
        else:
            return super().filter_queryset(request, queryset, view)
        