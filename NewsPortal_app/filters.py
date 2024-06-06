from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category

class NewsFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='любой'

    )
    created_after = DateTimeFilter(
        field_name='time_create',
        lookup_expr='gt',
        widget=DateTimeInput(format='%Y-%m-%dT%H:%M',
                             attrs={'type': 'datetime-local'})
    )
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
        }