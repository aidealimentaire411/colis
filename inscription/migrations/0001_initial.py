# Generated by Django 5.2.4 on 2025-07-20 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnneeScolaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=20, unique=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Symbole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50, unique=True)),
                ('icone', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('telephone', models.CharField(max_length=20)),
                ('carte_etudiant', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('annee_scolaire', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='inscription.anneescolaire')),
                ('symbole', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inscription.symbole')),
            ],
        ),
    ]
