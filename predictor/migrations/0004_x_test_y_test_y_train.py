# Generated by Django 3.0.3 on 2020-03-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0003_auto_20200316_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='X_test',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Days_1', models.FloatField()),
                ('Days_2', models.FloatField()),
                ('Days_3', models.FloatField()),
                ('Days_4', models.FloatField()),
                ('Days_5', models.FloatField()),
                ('Days_6', models.FloatField()),
                ('Days_7', models.FloatField()),
                ('Days_8', models.FloatField()),
                ('Days_9', models.FloatField()),
                ('Days_10', models.FloatField()),
                ('Days_11', models.FloatField()),
                ('Days_12', models.FloatField()),
                ('Days_13', models.FloatField()),
                ('Days_14', models.FloatField()),
                ('Days_15', models.FloatField()),
                ('Days_16', models.FloatField()),
                ('Days_17', models.FloatField()),
                ('Days_18', models.FloatField()),
                ('Days_19', models.FloatField()),
                ('Days_20', models.FloatField()),
                ('Days_21', models.FloatField()),
                ('Days_22', models.FloatField()),
                ('Days_23', models.FloatField()),
                ('Days_24', models.FloatField()),
                ('Days_25', models.FloatField()),
                ('Days_26', models.FloatField()),
                ('Days_27', models.FloatField()),
                ('Days_28', models.FloatField()),
                ('Days_29', models.FloatField()),
                ('Days_30', models.FloatField()),
                ('Days_31', models.FloatField()),
                ('Days_32', models.FloatField()),
                ('Days_33', models.FloatField()),
                ('Days_34', models.FloatField()),
                ('Days_35', models.FloatField()),
                ('Days_36', models.FloatField()),
                ('Days_37', models.FloatField()),
                ('Days_38', models.FloatField()),
                ('Days_39', models.FloatField()),
                ('Days_40', models.FloatField()),
                ('Days_41', models.FloatField()),
                ('Days_42', models.FloatField()),
                ('Days_43', models.FloatField()),
                ('Days_44', models.FloatField()),
                ('Days_45', models.FloatField()),
                ('Days_46', models.FloatField()),
                ('Days_47', models.FloatField()),
                ('Days_48', models.FloatField()),
                ('Days_49', models.FloatField()),
                ('Days_50', models.FloatField()),
                ('Days_51', models.FloatField()),
                ('Days_52', models.FloatField()),
                ('Days_53', models.FloatField()),
                ('Days_54', models.FloatField()),
                ('Days_55', models.FloatField()),
                ('Days_56', models.FloatField()),
                ('Days_57', models.FloatField()),
                ('Days_58', models.FloatField()),
                ('Days_59', models.FloatField()),
                ('Days_60', models.FloatField()),
                ('Days_61', models.FloatField()),
                ('Days_62', models.FloatField()),
                ('Days_63', models.FloatField()),
                ('Days_64', models.FloatField()),
                ('Days_65', models.FloatField()),
                ('Days_66', models.FloatField()),
                ('Days_67', models.FloatField()),
                ('Days_68', models.FloatField()),
                ('Days_69', models.FloatField()),
                ('Days_70', models.FloatField()),
                ('Days_71', models.FloatField()),
                ('Days_72', models.FloatField()),
                ('Days_73', models.FloatField()),
                ('Days_74', models.FloatField()),
                ('Days_75', models.FloatField()),
                ('Days_76', models.FloatField()),
                ('Days_77', models.FloatField()),
                ('Days_78', models.FloatField()),
                ('Days_79', models.FloatField()),
                ('Days_80', models.FloatField()),
                ('Days_81', models.FloatField()),
                ('Days_82', models.FloatField()),
                ('Days_83', models.FloatField()),
                ('Days_84', models.FloatField()),
                ('Days_85', models.FloatField()),
                ('Days_86', models.FloatField()),
                ('Days_87', models.FloatField()),
                ('Days_88', models.FloatField()),
                ('Days_89', models.FloatField()),
                ('Days_90', models.FloatField()),
                ('Days_91', models.FloatField()),
                ('Days_92', models.FloatField()),
                ('Days_93', models.FloatField()),
                ('Days_94', models.FloatField()),
                ('Days_95', models.FloatField()),
                ('Days_96', models.FloatField()),
                ('Days_97', models.FloatField()),
                ('Days_98', models.FloatField()),
                ('Days_99', models.FloatField()),
            ],
            options={
                'db_table': 'X_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='y_test',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Days_1', models.FloatField()),
                ('Days_2', models.FloatField()),
                ('Days_3', models.FloatField()),
                ('Days_4', models.FloatField()),
                ('Days_5', models.FloatField()),
                ('Days_6', models.FloatField()),
                ('Days_7', models.FloatField()),
                ('Days_8', models.FloatField()),
                ('Days_9', models.FloatField()),
                ('Days_10', models.FloatField()),
                ('Days_11', models.FloatField()),
                ('Days_12', models.FloatField()),
                ('Days_13', models.FloatField()),
                ('Days_14', models.FloatField()),
                ('Days_15', models.FloatField()),
                ('Days_16', models.FloatField()),
                ('Days_17', models.FloatField()),
                ('Days_18', models.FloatField()),
                ('Days_19', models.FloatField()),
                ('Days_20', models.FloatField()),
                ('Days_21', models.FloatField()),
                ('Days_22', models.FloatField()),
                ('Days_23', models.FloatField()),
                ('Days_24', models.FloatField()),
                ('Days_25', models.FloatField()),
                ('Days_26', models.FloatField()),
                ('Days_27', models.FloatField()),
                ('Days_28', models.FloatField()),
                ('Days_29', models.FloatField()),
                ('Days_30', models.FloatField()),
                ('Days_31', models.FloatField()),
                ('Days_32', models.FloatField()),
                ('Days_33', models.FloatField()),
                ('Days_34', models.FloatField()),
                ('Days_35', models.FloatField()),
                ('Days_36', models.FloatField()),
                ('Days_37', models.FloatField()),
                ('Days_38', models.FloatField()),
                ('Days_39', models.FloatField()),
                ('Days_40', models.FloatField()),
                ('Days_41', models.FloatField()),
                ('Days_42', models.FloatField()),
                ('Days_43', models.FloatField()),
                ('Days_44', models.FloatField()),
                ('Days_45', models.FloatField()),
                ('Days_46', models.FloatField()),
                ('Days_47', models.FloatField()),
                ('Days_48', models.FloatField()),
                ('Days_49', models.FloatField()),
                ('Days_50', models.FloatField()),
                ('Days_51', models.FloatField()),
                ('Days_52', models.FloatField()),
                ('Days_53', models.FloatField()),
                ('Days_54', models.FloatField()),
                ('Days_55', models.FloatField()),
                ('Days_56', models.FloatField()),
                ('Days_57', models.FloatField()),
                ('Days_58', models.FloatField()),
                ('Days_59', models.FloatField()),
                ('Days_60', models.FloatField()),
                ('Days_61', models.FloatField()),
                ('Days_62', models.FloatField()),
                ('Days_63', models.FloatField()),
                ('Days_64', models.FloatField()),
                ('Days_65', models.FloatField()),
                ('Days_66', models.FloatField()),
                ('Days_67', models.FloatField()),
                ('Days_68', models.FloatField()),
                ('Days_69', models.FloatField()),
                ('Days_70', models.FloatField()),
                ('Days_71', models.FloatField()),
                ('Days_72', models.FloatField()),
                ('Days_73', models.FloatField()),
                ('Days_74', models.FloatField()),
                ('Days_75', models.FloatField()),
                ('Days_76', models.FloatField()),
                ('Days_77', models.FloatField()),
                ('Days_78', models.FloatField()),
                ('Days_79', models.FloatField()),
                ('Days_80', models.FloatField()),
                ('Days_81', models.FloatField()),
                ('Days_82', models.FloatField()),
                ('Days_83', models.FloatField()),
                ('Days_84', models.FloatField()),
                ('Days_85', models.FloatField()),
                ('Days_86', models.FloatField()),
                ('Days_87', models.FloatField()),
                ('Days_88', models.FloatField()),
                ('Days_89', models.FloatField()),
                ('Days_90', models.FloatField()),
                ('Days_91', models.FloatField()),
                ('Days_92', models.FloatField()),
                ('Days_93', models.FloatField()),
                ('Days_94', models.FloatField()),
                ('Days_95', models.FloatField()),
                ('Days_96', models.FloatField()),
                ('Days_97', models.FloatField()),
                ('Days_98', models.FloatField()),
                ('Days_99', models.FloatField()),
            ],
            options={
                'db_table': 'y_test',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='y_train',
            fields=[
                ('ID', models.IntegerField(primary_key=True, serialize=False)),
                ('Date', models.DateField()),
                ('Days_1', models.FloatField()),
                ('Days_2', models.FloatField()),
                ('Days_3', models.FloatField()),
                ('Days_4', models.FloatField()),
                ('Days_5', models.FloatField()),
                ('Days_6', models.FloatField()),
                ('Days_7', models.FloatField()),
                ('Days_8', models.FloatField()),
                ('Days_9', models.FloatField()),
                ('Days_10', models.FloatField()),
                ('Days_11', models.FloatField()),
                ('Days_12', models.FloatField()),
                ('Days_13', models.FloatField()),
                ('Days_14', models.FloatField()),
                ('Days_15', models.FloatField()),
                ('Days_16', models.FloatField()),
                ('Days_17', models.FloatField()),
                ('Days_18', models.FloatField()),
                ('Days_19', models.FloatField()),
                ('Days_20', models.FloatField()),
                ('Days_21', models.FloatField()),
                ('Days_22', models.FloatField()),
                ('Days_23', models.FloatField()),
                ('Days_24', models.FloatField()),
                ('Days_25', models.FloatField()),
                ('Days_26', models.FloatField()),
                ('Days_27', models.FloatField()),
                ('Days_28', models.FloatField()),
                ('Days_29', models.FloatField()),
                ('Days_30', models.FloatField()),
                ('Days_31', models.FloatField()),
                ('Days_32', models.FloatField()),
                ('Days_33', models.FloatField()),
                ('Days_34', models.FloatField()),
                ('Days_35', models.FloatField()),
                ('Days_36', models.FloatField()),
                ('Days_37', models.FloatField()),
                ('Days_38', models.FloatField()),
                ('Days_39', models.FloatField()),
                ('Days_40', models.FloatField()),
                ('Days_41', models.FloatField()),
                ('Days_42', models.FloatField()),
                ('Days_43', models.FloatField()),
                ('Days_44', models.FloatField()),
                ('Days_45', models.FloatField()),
                ('Days_46', models.FloatField()),
                ('Days_47', models.FloatField()),
                ('Days_48', models.FloatField()),
                ('Days_49', models.FloatField()),
                ('Days_50', models.FloatField()),
                ('Days_51', models.FloatField()),
                ('Days_52', models.FloatField()),
                ('Days_53', models.FloatField()),
                ('Days_54', models.FloatField()),
                ('Days_55', models.FloatField()),
                ('Days_56', models.FloatField()),
                ('Days_57', models.FloatField()),
                ('Days_58', models.FloatField()),
                ('Days_59', models.FloatField()),
                ('Days_60', models.FloatField()),
                ('Days_61', models.FloatField()),
                ('Days_62', models.FloatField()),
                ('Days_63', models.FloatField()),
                ('Days_64', models.FloatField()),
                ('Days_65', models.FloatField()),
                ('Days_66', models.FloatField()),
                ('Days_67', models.FloatField()),
                ('Days_68', models.FloatField()),
                ('Days_69', models.FloatField()),
                ('Days_70', models.FloatField()),
                ('Days_71', models.FloatField()),
                ('Days_72', models.FloatField()),
                ('Days_73', models.FloatField()),
                ('Days_74', models.FloatField()),
                ('Days_75', models.FloatField()),
                ('Days_76', models.FloatField()),
                ('Days_77', models.FloatField()),
                ('Days_78', models.FloatField()),
                ('Days_79', models.FloatField()),
                ('Days_80', models.FloatField()),
                ('Days_81', models.FloatField()),
                ('Days_82', models.FloatField()),
                ('Days_83', models.FloatField()),
                ('Days_84', models.FloatField()),
                ('Days_85', models.FloatField()),
                ('Days_86', models.FloatField()),
                ('Days_87', models.FloatField()),
                ('Days_88', models.FloatField()),
                ('Days_89', models.FloatField()),
                ('Days_90', models.FloatField()),
                ('Days_91', models.FloatField()),
                ('Days_92', models.FloatField()),
                ('Days_93', models.FloatField()),
                ('Days_94', models.FloatField()),
                ('Days_95', models.FloatField()),
                ('Days_96', models.FloatField()),
                ('Days_97', models.FloatField()),
                ('Days_98', models.FloatField()),
                ('Days_99', models.FloatField()),
            ],
            options={
                'db_table': 'y_train',
                'managed': False,
            },
        ),
    ]
