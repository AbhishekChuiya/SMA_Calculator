from django.db import models

class FinancialData(models.Model):
    
    timeframe = models.IntegerField()
    datetime = models.DateTimeField()    
    close = models.DecimalField(max_digits=10, decimal_places=2)
