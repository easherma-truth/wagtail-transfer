from django.test import TestCase

from wagtail_transfer.operations import ImportPlanner
from tests.models import SimplePage, SponsoredPage


class TestImport(TestCase):
    fixtures = ['test.json']

    def test_import_pages(self):
        data = """{
            "ids_for_import": [
                ["wagtailcore.page", 12],
                ["wagtailcore.page", 15]
            ],
            "mappings": [
                ["wagtailcore.page", 12, "22222222-2222-2222-2222-222222222222"],
                ["wagtailcore.page", 15, "55555555-5555-5555-5555-555555555555"]
            ],
            "objects": [
                {
                    "model": "tests.simplepage",
                    "pk": 15,
                    "parent_id": 12,
                    "fields": {
                        "title": "Imported child page",
                        "show_in_menus": false,
                        "live": true,
                        "slug": "imported-child-page",
                        "intro": "This page is imported from the source site"
                    }
                },
                {
                    "model": "tests.simplepage",
                    "pk": 12,
                    "parent_id": 1,
                    "fields": {
                        "title": "Home",
                        "show_in_menus": false,
                        "live": true,
                        "slug": "home",
                        "intro": "This is the updated homepage"
                    }
                }
            ]
        }"""

        importer = ImportPlanner(12, None)
        importer.add_json(data)
        importer.run()

        updated_page = SimplePage.objects.get(url_path='/home/')
        self.assertEqual(updated_page.intro, "This is the updated homepage")

        created_page = SimplePage.objects.get(url_path='/home/imported-child-page/')
        self.assertEqual(created_page.intro, "This page is imported from the source site")

    def test_import_pages_with_fk(self):
        data = """{
            "ids_for_import": [
                ["wagtailcore.page", 12],
                ["wagtailcore.page", 15],
                ["wagtailcore.page", 16]
            ],
            "mappings": [
                ["wagtailcore.page", 12, "22222222-2222-2222-2222-222222222222"],
                ["wagtailcore.page", 15, "00017017-5555-5555-5555-555555555555"],
                ["wagtailcore.page", 16, "00e99e99-6666-6666-6666-666666666666"],
                ["tests.advert", 11, "adadadad-1111-1111-1111-111111111111"],
                ["tests.advert", 8, "adadadad-8888-8888-8888-888888888888"]
            ],
            "objects": [
                {
                    "model": "tests.simplepage",
                    "pk": 12,
                    "parent_id": 1,
                    "fields": {
                        "title": "Home",
                        "show_in_menus": false,
                        "live": true,
                        "slug": "home",
                        "intro": "This is the updated homepage"
                    }
                },
                {
                    "model": "tests.sponsoredpage",
                    "pk": 15,
                    "parent_id": 12,
                    "fields": {
                        "title": "Oil is still great",
                        "show_in_menus": false,
                        "live": true,
                        "slug": "oil-is-still-great",
                        "advert": 11,
                        "intro": "yay fossil fuels and climate change"
                    }
                },
                {
                    "model": "tests.advert",
                    "pk": 11,
                    "fields": {
                        "slogan": "put a leopard in your tank"
                    }
                },
                {
                    "model": "tests.sponsoredpage",
                    "pk": 16,
                    "parent_id": 12,
                    "fields": {
                        "title": "Eggs are great too",
                        "show_in_menus": false,
                        "live": true,
                        "slug": "eggs-are-great-too",
                        "advert": 8,
                        "intro": "you can make cakes with them"
                    }
                },
                {
                    "model": "tests.advert",
                    "pk": 8,
                    "fields": {
                        "slogan": "go to work on an egg"
                    }
                }
            ]
        }"""

        importer = ImportPlanner(12, None)
        importer.add_json(data)
        importer.run()

        updated_page = SponsoredPage.objects.get(url_path='/home/oil-is-still-great/')
        self.assertEqual(updated_page.intro, "yay fossil fuels and climate change")
        self.assertEqual(updated_page.advert.slogan, "put a leopard in your tank")

        created_page = SponsoredPage.objects.get(url_path='/home/eggs-are-great-too/')
        self.assertEqual(created_page.intro, "you can make cakes with them")
        self.assertEqual(created_page.advert.slogan, "go to work on an egg")