from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import CaseStudy, HowTo, CustomTag, TagCategory


@modeladmin_register
class HowToAdmin(ModelAdmin):
    model = HowTo
    menu_label = "How Tos"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ("title", "summary")


@modeladmin_register
class CaseStudyAdmin(ModelAdmin):
    model = CaseStudy
    menu_label = "Case Studies"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ("title", "summary")

@modeladmin_register
class TagCategoryAdmin(ModelAdmin):
    model = TagCategory
    menu_label = "Tag Categories"
    menu_icon = "list-ul"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)

@modeladmin_register
class CustomTagAdmin(ModelAdmin):
    model = CustomTag
    menu_label = "Tags"
    menu_icon = "tag"
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "category")
    search_fields = ("name", "category__name")

