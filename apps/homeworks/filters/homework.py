import django_filters
from apps.homeworks.models.homework_orm import HomeworkOrm


class HomeworkFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="exact")
    created_from = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_to = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    submitted_from = django_filters.DateTimeFilter(
        field_name="submitted_at", lookup_expr="gte"
    )
    submitted_to = django_filters.DateTimeFilter(
        field_name="submitted_at", lookup_expr="lte"
    )
    checked_from = django_filters.DateTimeFilter(
        field_name="checked_at", lookup_expr="gte"
    )
    checked_to = django_filters.DateTimeFilter(
        field_name="checked_at", lookup_expr="lte"
    )

    class Meta:
        model = HomeworkOrm
        fields = [
            "status",
            "created_from",
            "created_to",
            "submitted_from",
            "submitted_to",
            "checked_from",
            "checked_to",
        ]
