# Generated by Django 5.0.1 on 2024-04-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_produto_preco_marketing_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='descricao_curta',
            field=models.TextField(),
        ),
    ]