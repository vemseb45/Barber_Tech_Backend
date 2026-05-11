from django.db import migrations

def create_default_especialidades(apps, schema_editor):
    Especialidad = apps.get_model('barberias', 'Especialidad')
    especialidades_por_defecto = [
        'Cabello',
        'Barba',
        'Tratamientos',
        'Combos'
    ]
    for nombre in especialidades_por_defecto:
        Especialidad.objects.get_or_create(nombre=nombre)

def reverse_default_especialidades(apps, schema_editor):
    Especialidad = apps.get_model('barberias', 'Especialidad')
    Especialidad.objects.filter(nombre__in=['Cabello', 'Barba', 'Tratamientos', 'Combos']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('barberias', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_especialidades, reverse_default_especialidades),
    ]
