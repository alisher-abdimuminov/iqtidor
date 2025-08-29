from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models

from .models import (
    Answer,
    Block,
    Dtm,
    Subject,
    Test,
    Cefr,
    Question,
    QuestionAnswer,
    Banner,
    CEFRResult,
    DTMResult,
    Rash,
)


@admin.register(CEFRResult)
class CefrResultAdmin(ModelAdmin):
    list_display = ["author", "cefr", "rash", "degree"]


@admin.register(Rash)
class RashModelAdmin(ModelAdmin):
    list_display = ["cefr", "status"]


@admin.register(DTMResult)
class DtmResultAdmin(ModelAdmin):
    list_display = ["points"]


class AnswerInline(StackedInline):
    model = Answer
    extra = 0


class QuestionAnswerInline(StackedInline):
    model = QuestionAnswer
    extra = 0


@admin.register(Test)
class TestModelAdmin(ModelAdmin):
    list_display = ["type", "block"]
    inlines = [AnswerInline]
    list_filter = ["block"]
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }

    exclude = ("author", )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Block)
class BlockModelAdmin(ModelAdmin):
    list_display = [
        "name",
        "subject",
    ]
    
    exclude = ("author", )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Dtm)
class DtmModelAdmin(ModelAdmin):
    list_display = [
        "name",
        "created",
        "started",
        "ended",
    ]
    
    exclude = ("author", "participants", )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Subject)
class SubjectModelAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Cefr)
class CefrModelAdmin(ModelAdmin):
    list_display = [
        "name",
        "subject",
        "is_public",
    ]
    exclude = ("author", "participants", )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionModelAdmin(ModelAdmin):
    list_display = [
        "cefr",
        "type",
    ]
    inlines = [QuestionAnswerInline]
    
    exclude = ("author", )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change or not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Banner)
class BannerModelAdmin(ModelAdmin):
    list_display = ["description", "dtm", "cefr"]
