from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tags, TagsArticle


class TagsArticleInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            print(form)
            form.cleaned_data
            print(form.cleaned_data)
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
            raise ValidationError('Основной раздел может быть только один')
        return super().clean()  # вызываем базовый код переопределяемого метода


class TagsArticleInline(admin.TabularInline):
    model = TagsArticle


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [TagsArticleInline,]


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
