# Generated by Django 4.2.3 on 2023-07-29 07:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0004_answerdislike'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionDisLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_dislike', to='questions.questions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_dislike_question', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
