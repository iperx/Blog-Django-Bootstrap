from django.db import models
from django.urls import reverse


POST_MAX_LENGTH = 150
TAG_MAX_LENGTH = 50
# Equals to dash symbol plus Unix time length in seconds
SLUG_SUFFIX_LENGTH = 11


class Post(models.Model):
    """Post model"""

    title = models.CharField(
        verbose_name='Title', max_length=POST_MAX_LENGTH,
        db_index=True
    )
    slug = models.CharField(
        verbose_name='Slug', max_length=POST_MAX_LENGTH+SLUG_SUFFIX_LENGTH,
        db_index=True, blank=True, unique=True
    )
    body = models.TextField(verbose_name='Body', blank=True, db_index=True)
    date_pub = models.DateTimeField(
        verbose_name='Publication date', auto_now_add=True
    )
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def get_create_url(self):
        return reverse('post_create_url')

    def get_absolute_url(self):
        return reverse('post_details_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    """Tag model"""

    title = models.CharField(
        verbose_name='Title', max_length=TAG_MAX_LENGTH,
        db_index=True, unique=True
    )
    slug = models.CharField(
        verbose_name='Slug', max_length=TAG_MAX_LENGTH+SLUG_SUFFIX_LENGTH,
        db_index=True, blank=True, unique=True
    )

    def get_create_url(self):
        return reverse('tag_create_url')

    def get_absolute_url(self):
        return reverse('tag_details_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']