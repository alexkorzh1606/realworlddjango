from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'display_event_count', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', ]
    list_display_links = ['id', 'title', ]


@admin.register(models.Enroll)
class EnrollAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'created', ]
    list_select_related = ['event', ]
    list_display_links = ['id', 'user', 'event', ]


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'rate', 'created', 'updated', ]
    list_display_links = ['id', 'user', 'event', ]
    list_filter = ['created', 'event', ]
    readonly_fields = ['created', 'updated', 'id', ]


class EventReviewInline(admin.TabularInline):
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def get_readonly_fields(self, request, obj=None):
        return ['created', 'updated', ]
    model = models.Review
    extra = 0
    fields = ['user', 'rate', 'text', 'created', 'updated', ]



class PlacesLeftFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'places_left_filter'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', models.Event.EVENT_OCCUPANCY_LHALF),
            ('1', models.Event.EVENT_OCCUPANCY_GHALF),
            ('2', models.Event.EVENT_OCCUPANCY_SOLDOUT)
        )
        return filter_list

    def queryset(self, request, queryset):
        filter_value = self.value()
        list_id = []
        if filter_value is None:
            return queryset

        for value in queryset:
            if filter_value in value.estimate_places_left():
                list_id.append(value.id)
        return queryset.filter(id__in=list_id)


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'date_start', 'is_private', 'participants_number', 'display_enroll_count', 'display_places_left', ]
    list_display_links = ['id', 'title', ]
    search_fields = ['title', ]
    list_filter = [PlacesLeftFilter, 'category', 'features', ]
    ordering = ['date_start', ]
    fields = ['title', 'description', 'date_start', 'participants_number', 'is_private', 'category', 'features', 'display_enroll_count', 'display_places_left', ]
    readonly_fields = ['display_enroll_count', 'display_places_left', ]
    filter_horizontal = ('features', )
    inlines = [EventReviewInline]
