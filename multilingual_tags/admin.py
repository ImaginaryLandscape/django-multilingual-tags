"""Admin classes for the multilingual_tags app."""
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.generic import (
    BaseGenericInlineFormSet,
    GenericTabularInline,
)
from django.utils.translation import ugettext_lazy as _

from hvad.admin import TranslatableAdmin

from . import models


class TaggedItemInlineFormSet(BaseGenericInlineFormSet):
    model = models.TaggedItem

    def clean(self):
        cleaned_data = super(TaggedItemInlineFormSet, self).clean()
        # validate, that every tag is only used once
        tags = []
        for i in range(0, self.total_form_count()):
            tags.append(self.data.get('{0}-{1}-tag'.format(self.prefix, i)))
        if len(tags) != len(set(tags)):
            raise forms.ValidationError(_(
                'A Tag may only exist once per object.'))
        return cleaned_data


class TaggedItemInline(GenericTabularInline):
    formset = TaggedItemInlineFormSet
    model = models.TaggedItem
    extra = 1


class MultilingualTagsAdminMixin(object):
    """
    Mixin to provide a editing options for `Tag` items in the respective
    admin, this mixin is used in.

    """
    def get_inline_instances(self, request, obj=None):
        inline_instances = super(
            MultilingualTagsAdminMixin, self).get_inline_instances(
            request, obj)
        inline_instances.append(TaggedItemInline(self.model, self.admin_site))
        return inline_instances


admin.site.register(models.Tag, TranslatableAdmin)
admin.site.register(models.TaggedItem)
