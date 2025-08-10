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


@admin.register(Block)
class BlockModelAdmin(ModelAdmin):
    list_display = ["name", "subject", ]


@admin.register(Dtm)
class DtmModelAdmin(ModelAdmin):
    list_display = ["name", "created", "started", "ended", ]


@admin.register(Subject)
class SubjectModelAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(Cefr)
class CefrModelAdmin(ModelAdmin):
    list_display = ["name", "subject", "is_public",]


@admin.register(Question)
class QuestionModelAdmin(ModelAdmin):
    list_display = ["cefr", "type",]
    inlines = [QuestionAnswerInline]


@admin.register(Banner)
class BannerModelAdmin(ModelAdmin):
    list_display = ["description", "dtm", "cefr"]
