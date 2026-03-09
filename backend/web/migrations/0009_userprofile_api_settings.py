from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_rename_prompts_systemprompt_prompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='api_base',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='api_key',
            field=models.TextField(blank=True, default=''),
        ),
    ]
