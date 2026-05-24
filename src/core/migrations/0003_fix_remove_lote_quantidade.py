from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('core', '0002_remove_lote_quantidade_produto_quantidade_total')]
    operations = [
        migrations.AddField(
            model_name='lote',
            name='quantidade',
            field=models.PositiveIntegerField(default=0),
        ),
    ]