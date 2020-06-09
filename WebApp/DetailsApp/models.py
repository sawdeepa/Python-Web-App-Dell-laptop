from django.db import models
from django.utils import timezone

class Master(models.Model):
     IDMD= models.CharField(max_length=1200,unique=True)
     Domain = models.CharField(max_length=1200)

     def _str_(self):
         return self.IDMD

class Category(models.Model):
      IDCat = models.CharField(max_length=1200,unique=True)
      Category = models.CharField(max_length=1200, blank=False)

      def _str_(self):
          return self.IDCat

class Rule(models.Model):
    Graphs=(
        ('1' ,'Pie chart'),
        ('4','Line chart'),
        ('5','Y-axis Bar Chart'),
        ('6','Bubble Chart'),
        ('7','Scatter Plot'),
        ('8','Area Chart'),
        ('9','Donut Graph'),
        ('10','Xaxis Barchart'),
        ('11','TreeMap'),
        ('12','Gauge Chart'),
        ('14','Histogram')

    )
    IDM = models.CharField(max_length=1200,blank=False, null=False,unique=True)
    Domain = models.CharField(max_length=1200, blank=True)
    Insight = models.CharField(max_length=1200, blank=True)
    BusinessImplication= models.CharField(max_length=1500, blank=True)
    Query = models.CharField(max_length=1200, blank=True)
    VQuery = models.CharField(max_length=1200, blank=True)
    Recordcount = models.CharField(max_length=1200, blank=True)
    LastRefreshedOn = models.DateTimeField(default=timezone.now )
    GraphValue = models.CharField(max_length=1200, blank=True,choices=Graphs)
    Xaxis = models.CharField(max_length=1200, blank=True)
    Yaxis = models.CharField(max_length=1200, blank=True)
    Subtitle = models.CharField(max_length=1200, blank=True)
    DomainID = models.ForeignKey(Master, default=5, on_delete=models.SET_DEFAULT,related_name='Masters')
    CategoryID = models.ForeignKey(Category, default=1, on_delete=models.SET_DEFAULT,related_name='Categories')

    def _str_(self):
        return self.IDM
