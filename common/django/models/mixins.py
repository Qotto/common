# coding: utf-8
# Copyright (c) Qotto, 2017

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from humanize import naturaltime
from secrets import token_urlsafe
from common.django import fields

__all__ = [
    'LockableMixin',
    'ArchivableMixin',
    'EditedTimeMixin',
    'ExternalReferenceMixin',
    'LatLonMixin',
]

class LockableMixin(models.Model):
    class Meta:
        abstract = True

    @property
    def queryset(self):
        return self.__class__.objects.filter(pk=self.pk)

    def lock(self):
        self.queryset.select_for_update().exists()

    def update(self, *args, **kwargs):
        self.queryset.update(*args, **kwargs)


class ArchivableMixin(models.Model):
    archived = models.CharField(_("archived state"), max_length=32, blank=True)
    archived_date = models.DateTimeField(_("archived on"), null=True, editable=False)
    restored_date = models.DateTimeField(_("restored on"), null=True, editable=False)

    class Meta:
        abstract = True

    def get_existing_display(self) -> bool:
        return not self.archived
    get_existing_display.short_description = _("existing") # type: ignore
    get_existing_display.boolean = True # type: ignore

    def archive(self) -> None:
        self.archived = token_urlsafe(24)
        self.archived_date = timezone.now()
        self.full_clean()
        self.save(update_fields=['archived', 'archived_date'])

    def restore(self) -> None:
        self.archived = ''
        self.restored_date = timezone.now()
        self.full_clean()
        self.save(update_fields=['archived', 'restored_date'])


class EditedTimeMixin(models.Model):
    date_created = models.DateTimeField(_("created on"), auto_now_add=True)
    date_updated = models.DateTimeField(_("updated on"), auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if 'update_fields' in kwargs:
            kwargs['update_fields'] = list(set(kwargs['update_fields'] + ['date_updated']))
        return super(EditedTimeMixin, self).save(*args, **kwargs)

    def date_updated_display(self) -> str:
        return naturaltime(timezone.now() - self.date_updated)


class ExternalReferenceMixin(models.Model):
    ext_source = models.CharField(_("external source"), max_length=40, blank=True)
    ext_id = models.CharField(_("external ID"), max_length=32, blank=True)

    class Meta:
        abstract = True


class LatLonMixin(models.Model):
    lat = fields.RoundedDecimalField(_("latitude"), max_digits=10, decimal_places=7, default=0)
    lon = fields.RoundedDecimalField(_("longitude"), max_digits=10, decimal_places=7, default=0)

    class Meta:
        abstract = True