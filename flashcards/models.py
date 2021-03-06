from django.db import models
from django.contrib.auth.models import User

units = [('seconds', 'seconds'), ('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days'), ('months', 'months')]


class Bin(models.Model):
    # order is the order of the bins when moving cards up or down
    order = models.IntegerField()
    # amount of units to wait
    amount = models.IntegerField()
    # unit needs to be something that works as a parameter to timedelta (relativedelta), e.g. minutes, hours, months,..
    unit = models.CharField(max_length=10, choices=units)

    def __str__(self):
        return str(self.order)


class Card(models.Model):
    word = models.TextField()
    definition = models.TextField()
    next_review = models.DateTimeField(null=True, blank=True)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, null=True, blank=True)
    total_wrong = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.word
