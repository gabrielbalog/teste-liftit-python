from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=150)
    registration = models.CharField(verbose_name=_("registration"), max_length=150)
    brand = models.CharField(verbose_name=_("brand"), max_length=150)
    type = models.CharField(verbose_name=_("type"), max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("owner"))

    def __str__(self):
        return f"{self.name} - {self.owner}"
