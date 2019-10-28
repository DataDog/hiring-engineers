from datetime import date, timedelta

from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
from django.utils import timezone


#Helper methods to set default dates
from django.utils.datetime_safe import datetime

from user.models import User


class ProgramPeriod(models.Model):

    name = models.CharField(max_length=60, blank=False)
    start = models.DateField(default=get_first_day(timezone.now()))
    end = models.DateField(default= get_last_day(timezone.now()))

    def __str__(self):
        return 'Program Period: {}'.format(self.name)
    class Meta:
        ordering = ('-start',)


class ModelYear(models.Model):
    year = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return '{}'.format(self.year)
    class Meta:
        ordering = ('-year',)



class VehicleModel(models.Model):
    year = models.ForeignKey(ModelYear,
                             related_name='vehicle_models',
                             on_delete=models.CASCADE,
                             null=False)

    name = models.CharField(max_length=80, blank=False)
    description = models.CharField(max_length=120, blank=True)
    weight = models.PositiveIntegerField(blank=False)
    inception = models.DecimalField(max_digits=8, decimal_places=6)
    addl_miles = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return '{}. {} {} {} {} {}'.format( self.year, self.name, self.description, self.weight, self.inception, self.addl_miles)

    class Meta:
        ordering = ( 'year', 'name',)


class ModelProgram(models.Model):

    vehicle_model = models.ForeignKey(VehicleModel, related_name='model_programs', on_delete=models.CASCADE, null=False)
    program_period = models.ForeignKey(ProgramPeriod, related_name='model_programs', on_delete=models.CASCADE, null=False)

    lease_money_factor = models.DecimalField(max_digits=8, decimal_places=6)
    retail_rate = models.DecimalField(max_digits=6, decimal_places=6)
    residual_24 = models.DecimalField(max_digits=6, decimal_places=6)
    residual_30 = models.DecimalField(max_digits=6, decimal_places=6)
    residual_36 = models.DecimalField(max_digits=6, decimal_places=6)
    residual_42 = models.DecimalField(max_digits=6, decimal_places=6)
    lease_money = models.DecimalField(max_digits = 10, decimal_places=2)
    apr_money = models.DecimalField(max_digits = 10, decimal_places=2)
    loyalty_money = models.DecimalField(max_digits = 10, decimal_places=2)
    conquest_money = models.DecimalField(max_digits = 10, decimal_places=2)

    def __str__(self):
        return '{} {} {}'.format(self.vehicle_model.year.year, self.vehicle_model.name, self.program_period.name)

    class Meta:
        ordering = ('program_period', 'vehicle_model',)








