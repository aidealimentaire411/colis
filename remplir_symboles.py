import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aide_alim.settings')
django.setup()

from inscription.models import Symbole

symboles = [
    ('sapin', '🎄'),
    ('avion', '✈️'),
    ('etoile', '⭐'),
    ('soleil', '🌞'),
    ('lune', '🌙'),
    ('rose', '🌹'),
    ('dauphin', '🐬'),
    ('coeur', '❤️'),
    ('fraise', '🍓'),
    ('souris', '🐭'),
    ('banane', '🍌'),
    ('chocolat', '🍫'),
    ('bateau', '⛵'),
    ('orange', '🍊'),
    ('pomme', '🍎'),
    ('scorpion', '🦂'),
    ('raisin', '🍇'),
    ('ballon', '🎈'),
]

for nom, icone in symboles:
    obj, created = Symbole.objects.get_or_create(nom=nom, defaults={'icone': icone})
    if created:
        print(f"Symbole créé : {nom} {icone}")
    else:
        print(f"Symbole déjà existant : {nom}")
