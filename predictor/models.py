# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings

from ndarray import NDArrayField
from datetime import datetime
from sqlalchemy import create_engine

import pandas as pd

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']
 
database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name,
)

heroku_db = 'postgres://hfqxspbjkknhoh:4b5c72fe18d750fa3b2a96c904c3ecd8608577086a75620e650ce14f3b25690f@ec2-54-81-37-115.compute-1.amazonaws.com:5432/ddrv4lrinua85j'

engine = create_engine(database_url, echo=False)

# Create your models here.

class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending hour must be after the starting hour')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))


class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username,self.password

class Index(models.Model):
    stock = models.CharField(max_length=100)
    start_date = models.CharField(max_length=100,default='2002-01-01')
    end_date = models.CharField(max_length=100,default=str(datetime.now().date()))
    
    def __str__(self):
        return self.stock, self.start_date,self.end_date,
    

class save_data(models.Model):
    csv = models.CharField(max_length=100)
    X_train = NDArrayField()
    X_test = NDArrayField()
    y_train = NDArrayField()
    y_test = NDArrayField()
  

    def __str__(self):
        return self.csv
    def __repr__(self):
        return self.X_train,self.X_test,self.y_train,self.y_test


class DFModel(models.Model):
    ID = models.IntegerField(primary_key=True)
    Open = models.FloatField() # min: 16.14, max: 923.5, mean: 191.94412464124642
    High = models.FloatField() # min: 16.63, max: 968.99, mean: 195.48554325543256
    Low = models.FloatField() # min: 14.98, max: 901.02, mean: 188.33346043460435
    Close = models.FloatField() # min: 15.8, max: 917.42, mean: 192.04155801558014
    Volume = models.IntegerField() # min: 118500, max: 60938800, mean: 5729508.938089381
    Dividends = models.PositiveSmallIntegerField() # min: 0, max: 0, mean: 0.0
    Stock_splits = models.PositiveSmallIntegerField() # min: 0, max: 0, mean: 0.0

    class Meta:
        db_table = 'DFModel'
        managed = False

class PCT_Change(models.Model):
    ID = models.IntegerField(primary_key=True)
    Date = models.DateField(blank=True,null=True)
    Days_0 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001528541330630026
    Days_1 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0015331132757228738
    Days_2 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0015650890058157157
    Days_3 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016940887412607343
    Days_4 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018032491921580738
    Days_5 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018109124711248009
    Days_6 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001751132275548934
    Days_7 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017509658831329454
    Days_8 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001759425455365466
    Days_9 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.00172997066514825
    Days_10 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016956541287769771
    Days_11 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016942430207256525
    Days_12 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016907442774014244
    Days_13 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001676198561776723
    Days_14 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017095820349374439
    Days_15 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017213233297371856
    Days_16 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017108496348014243
    Days_17 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017003010030532965
    Days_18 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017111077968624533
    Days_19 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001722697051436696
    Days_20 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017165269582970078
    Days_21 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017357618099468057
    Days_22 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017356946466511966
    Days_23 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017178886308926314
    Days_24 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016706851877222925
    Days_25 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001688323327398045
    Days_26 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0016951657796537172
    Days_27 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001716180792119711
    Days_28 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017142245446163753
    Days_29 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017330060050855958
    Days_30 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017600331454178117
    Days_31 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017631606476251616
    Days_32 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017423004260708323
    Days_33 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017387165389570274
    Days_34 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017349345725257818
    Days_35 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017550982241687917
    Days_36 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017593643140622
    Days_37 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017607687733864593
    Days_38 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001736232415484158
    Days_39 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017834519239778076
    Days_40 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017650911622027652
    Days_41 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017842465170797902
    Days_42 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.00179714370008415
    Days_43 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017950988247479244
    Days_44 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001817809125212522
    Days_45 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001802702126296613
    Days_46 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017956848539569068
    Days_47 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001795333040373754
    Days_48 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017901261755095142
    Days_49 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017863832312387882
    Days_50 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018024280540263568
    Days_51 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018261940972119797
    Days_52 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018227753362204193
    Days_53 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018310925418204616
    Days_54 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018347124631490257
    Days_55 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018455361690262208
    Days_56 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001857173996331895
    Days_57 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001881346706975542
    Days_58 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018978368973907626
    Days_59 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019009212428894439
    Days_60 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019034549123491452
    Days_61 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001889192855962805
    Days_62 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019107360593749324
    Days_63 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019100899688649778
    Days_64 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019005047953261347
    Days_65 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019254753512871917
    Days_66 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001916367673849655
    Days_67 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019150798621118653
    Days_68 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019230410593164054
    Days_69 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019802988175226964
    Days_70 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019874221107288605
    Days_71 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002072297799420022
    Days_72 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0021348218861111635
    Days_73 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020615461212249104
    Days_74 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002063503095761203
    Days_75 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020586343808616085
    Days_76 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002076188557543427
    Days_77 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002084342053720379
    Days_78 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002084231970551283
    Days_79 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020918763914758148
    Days_80 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020877038548045776
    Days_81 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002119446835666941
    Days_82 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002146102848259167
    Days_83 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0021272924510089197
    Days_84 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0021352368870834987
    Days_85 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002099553220867962
    Days_86 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020691314720026727
    Days_87 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.002066272331968923
    Days_88 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0020147907952611315
    Days_89 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019974334529716245
    Days_90 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019843977957526354
    Days_91 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019933634597042523
    Days_92 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001986220590478364
    Days_93 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0019779906448723606
    Days_94 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018836608909804835
    Days_95 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001844938142029585
    Days_96 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018437453168404167
    Days_97 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0018226821411415485
    Days_98 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.0017887725614472913
    Days_99 = models.FloatField() # min: -0.1932743362831859, max: 0.24395052876859658, mean: 0.001780758969684236

    class Meta:
        db_table = 'PCT_Change'
        managed = False


class Xtest(models.Model):
    ID = models.IntegerField(primary_key=True)
    Days_1 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016818867254741975
    Days_2 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014812052812691945
    Days_3 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014126914185531544
    Days_4 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017266114236012963
    Days_5 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0026802622314005048
    Days_6 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001548309753445869
    Days_7 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0022629894906253
    Days_8 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002459462883551195
    Days_9 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001377549185230977
    Days_10 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014881880735900337
    Days_11 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021869442548794146
    Days_12 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002029284842979134
    Days_13 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016466475226323066
    Days_14 = models.FloatField() # min: -0.1508806912595546, max: 0.1920422249289484, mean: 0.0015719107079247034
    Days_15 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019663943721833395
    Days_16 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0015442058602952418
    Days_17 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015434323753072045
    Days_18 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0015052361925751336
    Days_19 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0016893818719895762
    Days_20 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001515649065272068
    Days_21 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0019315943358997943
    Days_22 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.0015263348621126181
    Days_23 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0013766566884102379
    Days_24 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016370583799534837
    Days_25 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014220534641111412
    Days_26 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015862816052173879
    Days_27 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0018465406340541352
    Days_28 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016007774851537913
    Days_29 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0022031723451273327
    Days_30 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019848891335115058
    Days_31 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016725636477279609
    Days_32 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016586874074217119
    Days_33 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020629790943714754
    Days_34 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0014448231968999601
    Days_35 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019434566827502206
    Days_36 = models.FloatField() # min: -0.1508806912595546, max: 0.1920422249289484, mean: 0.0013577711716868076
    Days_37 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0013066009634782833
    Days_38 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019048333972169619
    Days_39 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0013793612301798597
    Days_40 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0024487080260622188
    Days_41 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0018034655679042232
    Days_42 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018726931932250745
    Days_43 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015554274744951158
    Days_44 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021293030062233807
    Days_45 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0022301419978977767
    Days_46 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0008006449640107754
    Days_47 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019868216005837994
    Days_48 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.00246840671724026
    Days_49 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015979935734690698
    Days_50 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015029408347586658
    Days_51 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021517348624382118
    Days_52 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002372296026056434
    Days_53 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021312571800097936
    Days_54 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.001983820765261592
    Days_55 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017839352671960263
    Days_56 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014223007787209025
    Days_57 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019370971748904884
    Days_58 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0022190210339654605
    Days_59 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0018991282886993799
    Days_60 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.002524811107084294
    Days_61 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015858937307280361
    Days_62 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002505862937341687
    Days_63 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020246571912640433
    Days_64 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.001967220037533513
    Days_65 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0017048435841575625
    Days_66 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019819108591472233
    Days_67 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0012500087518516332
    Days_68 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.0022546515862359668
    Days_69 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017523058671864815
    Days_70 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018939851921489393
    Days_71 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014400313782206953
    Days_72 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001935779120724719
    Days_73 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002394874972631455
    Days_74 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002304767643587614
    Days_75 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.0022330815612922644
    Days_76 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002362531706769805
    Days_77 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0026192483952391064
    Days_78 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021056627473482357
    Days_79 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016680103561189416
    Days_80 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.002521275345807635
    Days_81 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.00196626488825919
    Days_82 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018605561627524545
    Days_83 = models.FloatField() # min: -0.17175839289337802, max: 0.19894861429208224, mean: 0.0026921522802976204
    Days_84 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020109529040666704
    Days_85 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.002278584240672695
    Days_86 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.0022054190081478575
    Days_87 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.002365449996699162
    Days_88 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019299551453671223
    Days_89 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002192661075996368
    Days_90 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018928995151147267
    Days_91 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001831827143927785
    Days_92 = models.FloatField() # min: -0.17175839289337802, max: 0.19894861429208224, mean: 0.002011037930693904
    Days_93 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0024918038128473106
    Days_94 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002032799306142319
    Days_95 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002135054007746899
    Days_96 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.0018478024230773745
    Days_97 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.001647996097046774
    Days_98 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018441558759055927
    Days_99 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0013225881589762271
    
    class Meta:
        db_table = 'Xtest'
        managed = False


class Xtrain(models.Model):
    ID = models.IntegerField(primary_key=True)
   
    Days_1 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016818867254741975
    Days_2 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014812052812691945
    Days_3 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014126914185531544
    Days_4 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017266114236012963
    Days_5 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0026802622314005048
    Days_6 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001548309753445869
    Days_7 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0022629894906253
    Days_8 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002459462883551195
    Days_9 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001377549185230977
    Days_10 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014881880735900337
    Days_11 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021869442548794146
    Days_12 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002029284842979134
    Days_13 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016466475226323066
    Days_14 = models.FloatField() # min: -0.1508806912595546, max: 0.1920422249289484, mean: 0.0015719107079247034
    Days_15 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019663943721833395
    Days_16 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0015442058602952418
    Days_17 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015434323753072045
    Days_18 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0015052361925751336
    Days_19 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0016893818719895762
    Days_20 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001515649065272068
    Days_21 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0019315943358997943
    Days_22 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.0015263348621126181
    Days_23 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0013766566884102379
    Days_24 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016370583799534837
    Days_25 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014220534641111412
    Days_26 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015862816052173879
    Days_27 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0018465406340541352
    Days_28 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016007774851537913
    Days_29 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0022031723451273327
    Days_30 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019848891335115058
    Days_31 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016725636477279609
    Days_32 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016586874074217119
    Days_33 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020629790943714754
    Days_34 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0014448231968999601
    Days_35 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019434566827502206
    Days_36 = models.FloatField() # min: -0.1508806912595546, max: 0.1920422249289484, mean: 0.0013577711716868076
    Days_37 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0013066009634782833
    Days_38 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019048333972169619
    Days_39 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0013793612301798597
    Days_40 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0024487080260622188
    Days_41 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0018034655679042232
    Days_42 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018726931932250745
    Days_43 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015554274744951158
    Days_44 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021293030062233807
    Days_45 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0022301419978977767
    Days_46 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0008006449640107754
    Days_47 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019868216005837994
    Days_48 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.00246840671724026
    Days_49 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015979935734690698
    Days_50 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015029408347586658
    Days_51 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021517348624382118
    Days_52 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002372296026056434
    Days_53 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021312571800097936
    Days_54 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.001983820765261592
    Days_55 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017839352671960263
    Days_56 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014223007787209025
    Days_57 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019370971748904884
    Days_58 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.0022190210339654605
    Days_59 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0018991282886993799
    Days_60 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.002524811107084294
    Days_61 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0015858937307280361
    Days_62 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002505862937341687
    Days_63 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020246571912640433
    Days_64 = models.FloatField() # min: -0.1508806912595546, max: 0.2439505287685965, mean: 0.001967220037533513
    Days_65 = models.FloatField() # min: -0.1932743362831859, max: 0.1920422249289484, mean: 0.0017048435841575625
    Days_66 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019819108591472233
    Days_67 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0012500087518516332
    Days_68 = models.FloatField() # min: -0.14507098014818165, max: 0.2439505287685965, mean: 0.0022546515862359668
    Days_69 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0017523058671864815
    Days_70 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018939851921489393
    Days_71 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0014400313782206953
    Days_72 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001935779120724719
    Days_73 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002394874972631455
    Days_74 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002304767643587614
    Days_75 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.0022330815612922644
    Days_76 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002362531706769805
    Days_77 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0026192483952391064
    Days_78 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0021056627473482357
    Days_79 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0016680103561189416
    Days_80 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.002521275345807635
    Days_81 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.00196626488825919
    Days_82 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018605561627524545
    Days_83 = models.FloatField() # min: -0.17175839289337802, max: 0.19894861429208224, mean: 0.0026921522802976204
    Days_84 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0020109529040666704
    Days_85 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.002278584240672695
    Days_86 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.0022054190081478575
    Days_87 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.002365449996699162
    Days_88 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0019299551453671223
    Days_89 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002192661075996368
    Days_90 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018928995151147267
    Days_91 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.001831827143927785
    Days_92 = models.FloatField() # min: -0.17175839289337802, max: 0.19894861429208224, mean: 0.002011037930693904
    Days_93 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0024918038128473106
    Days_94 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002032799306142319
    Days_95 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.002135054007746899
    Days_96 = models.FloatField() # min: -0.1932743362831859, max: 0.19894861429208224, mean: 0.0018478024230773745
    Days_97 = models.FloatField() # min: -0.17175839289337802, max: 0.2439505287685965, mean: 0.001647996097046774
    Days_98 = models.FloatField() # min: -0.1932743362831859, max: 0.2439505287685965, mean: 0.0018441558759055927
    Days_99 = models.FloatField() # min: -0.1932743362831859, max: 0.17669231977383393, mean: 0.0013225881589762271
    
    class Meta:
        db_table = 'Xtrain'
        managed = False


class Ytrain(models.Model):
    ID = models.IntegerField(primary_key=True)
    Days_0 = models.FloatField()
    
    class Meta:
        db_table = 'Ytrain'
        managed = False

class Ytest(models.Model):
    ID = models.IntegerField(primary_key=True)

    Days_0 = models.FloatField()
  
    class Meta:
        db_table = 'Ytest'
        managed = False

class Pred(models.Model):
    ID = models.IntegerField(primary_key=True)
    pred = models.FloatField()

    class Meta:
        db_table = "Pred"
        managed = False