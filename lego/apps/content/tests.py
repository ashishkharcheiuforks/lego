from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from lego.apps.articles.models import Article
from lego.apps.content.models import SlugModel
from lego.apps.users.models import User
from lego.utils.test_utils import BaseTestCase


class ExampleSlugContent(SlugModel):
    slug_field = "title"
    title = models.CharField(max_length=255)


class SlugModelTestCase(BaseTestCase):
    def test_slug(self):
        item = ExampleSlugContent(title="CORRECTSLUG")
        self.assertIsNone(item.slug)
        item.save()
        self.assertNotEqual("{}-CORRECTSLUG".format(item.id), item.slug)
        self.assertEqual("{}-correctslug".format(item.id), item.slug)
        self.assertEqual(slugify("{}-CORRECTSLUG".format(item.id)), item.slug)

    def test_slug_slice(self):
        item = ExampleSlugContent(
            title="hey, come to this cool event and get free drinks all night"
        )
        item.save()
        self.assertEqual(
            "{}-hey-come-to-this-cool-event-and-get-free-drinks".format(item.id),
            item.slug,
        )

    def test_slug_slice_when_word_ends_at_max_len(self):
        item = ExampleSlugContent(
            title="hey, come to this cool event and get free driiiiinks heh"
        )
        item.save()
        self.assertEqual(
            "{}-hey-come-to-this-cool-event-and-get-free".format(item.id), item.slug
        )

    def test_slug_static(self):
        item = ExampleSlugContent(
            title="hey come to this cool event and get free drinks all night"
        )
        item.save()
        item.title = "hi"
        item.save()
        self.assertEqual(
            "{}-hey-come-to-this-cool-event-and-get-free-drinks".format(item.id),
            item.slug,
        )


class ContentModelTestCase(BaseTestCase):
    fixtures = [
        "test_abakus_groups.yaml",
        "initial_files.yaml",
        "development_users.yaml",
        "test_articles.yaml",
    ]

    def test_parse_content(self):
        content = (
            "<p>some <b>cool</b> text telling you to come to this party</p>"
            "<p>psst.. We got free <strike>dranks!</strike>drinks</p>"
        )
        article = Article.objects.create(
            title="test content",
            description="test description",
            text=content,
            current_user=User.objects.get(username="webkom"),
        )
        article.refresh_from_db()
        self.assertEqual(article.text, content)

    def test_parse_content_strip_unsafe_values(self):
        content = """
            <p>some <b>cool</b> text telling you to come to this party</p>
            <p><script>window.alert("I am a virus")</script></p>
        """
        article = Article.objects.create(
            title="test content",
            description="test description",
            text=content,
            current_user=User.objects.get(username="webkom"),
        )
        article.refresh_from_db()
        self.assertTrue("<script>" not in article.text)

    def test_parse_content_strip_css_values(self):
        content = """
            <p>some <b>cool</b> text telling you to come to this party</p>
            <p style="color: red;">psst.. We got free <strike>dranks!</strike>drinks</p>
        """
        article = Article.objects.create(
            title="test content",
            description="test description",
            text=content,
            current_user=User.objects.get(username="webkom"),
        )
        article.refresh_from_db()
        self.assertTrue('style="color: red;"' not in article.text)

    def test_parse_content_handle_images(self):
        content = """
            <p>some <b>cool</b> text telling you to come to this party</p>
            <p><img data-file-key="default_male_avatar.png" src="dont_store_this_url.png" /></p>
            <p>psst.. We got free <strike>dranks!</strike>drinks</p>
        """

        article = Article.objects.create(
            title="test content",
            description="test description",
            text=content,
            current_user=User.objects.get(username="webkom"),
        )
        article.refresh_from_db()
        self.assertFalse("src" in article.text)

    def test_parse_content_handle_private_files(self):
        content = """
            <p>some <b>cool</b> text telling you to come to this party</p>
            <p><img data-file-key="not_public.png" src="dont_store_this_url.png" /></p>
            <p><img data-file-key="default_female_avatar.png" src="img.png" /></p>
            <p>psst.. We got free <strike>dranks!</strike>drinks</p>
        """

        with self.assertRaises(ValidationError):
            Article.objects.create(
                title="test content",
                description="test description",
                text=content,
                current_user=User.objects.get(username="webkom"),
            )

    def test_parse_content_handle_missing_files(self):
        content = """
            <p>some <b>cool</b> text telling you to come to this party</p>
            <p><img data-file-key="2234521.png" src="1.png" /></p>
            <p><img data-file-key="22345551.png" src="2.png" /></p>
            <p>psst.. We got free <strike>dranks!</strike>drinks</p>
        """

        with self.assertRaises(ValidationError):
            Article.objects.create(
                title="test content",
                description="test description",
                text=content,
                current_user=User.objects.get(username="webkom"),
            )
