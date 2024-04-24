# Generated by Django 3.2 on 2024-04-24 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kinobd', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='actor',
            new_name='country_film',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='critic',
            new_name='film_genre',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='critic_rating',
            new_name='imdb_ratings_count',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='country',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='marketing',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='premiere',
        ),
        migrations.AddField(
            model_name='movie',
            name='actors',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_rating',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='negative_ratings',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='original_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='positive_ratings',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='premiere_date',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rating',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='budget',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating_count',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='russian_gross',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='worldwide_gross',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]