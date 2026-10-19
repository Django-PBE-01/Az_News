from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('news', '0003_remove_news_is_top')]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField(max_length=5000)),
            ],
            options={'verbose_name': 'Contact message', 'verbose_name_plural': 'Contact messages', 'ordering': ('-created_at',)},
        ),
    ]
