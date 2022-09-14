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
        return ['id', 'created', 'updated', ]
    model = models.Review
    extra = 0
    fields = ['id', 'user', 'event', 'rate', 'text', 'created', 'updated', ]


class PlacesLeftFilter(admin.SimpleListFilter):
    title = 'Заполненность'
    parameter_name = 'places_left_filter'

    def lookups(self, request, model_admin):
        filter_list = (
            ('0', '<= 50%'),
            ('1', '> 50%'),
            ('2', 'sold-out')
        )
        return filter_list

    def queryset(self, request, queryset):
        filter_value = self.value()
        # if filter_value == '0':
        #     return queryset.filter(__gt=0, __lte=0.5)
        # if filter_value == '1':
        #     return queryset.filter(occupancy_estimation_prop__gt=0.5)
        # if filter_value == '2':
        #     return queryset.filter(places_left_prop=0)
        return queryset


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    # TODO Также требуется реализовать собственный фильтр: “Заполненность”
    list_display = ['id', 'title', 'date_start', 'participants_number', 'is_private', 'category', 'display_enroll_count', 'display_places_left', ]
    search_fields = ['title', ]
    list_filter = [PlacesLeftFilter, 'category', 'features', ]
    ordering = ['date_start', ]
    fields = ['title', 'description', 'date_start', 'participants_number', 'is_private', 'category', 'features', 'show_enroll_count', 'show_places_left', ]
    readonly_fields = ['show_enroll_count', 'show_places_left', ]
    filter_horizontal = ('features', )
    inlines = [EventReviewInline]
