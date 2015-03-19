from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.models.loading import get_model

import os
import json
from datetime import datetime


class Command(BaseCommand):
    args = "<fixturename>"
    help = "Loads a json-fixture incrementally, that is without needing to flush the DB to load a tiny fixture change"

    def handle(self, *args, **options):
        try:
            fixturename = args[0]
        except IndexError:
            raise CommandError("No fixture provided")

        # Search the fixture
        for app in settings.INSTALLED_APPS:
            if app.startswith("django.contrib"):
                continue  # Don't care for contrib apps, since they don't have fixtures
            if os.path.isfile(os.path.join(settings.BASE_DIR, app, "fixtures", fixturename)):
                fixturefile = os.path.join(settings.BASE_DIR, app, "fixtures", fixturename)
                break
            # Omitting .json is cool, too
            if os.path.isfile(os.path.join(settings.BASE_DIR, app, "fixtures", fixturename+".json")):
                fixturefile = os.path.join(settings.BASE_DIR, app, "fixtures", fixturename+".json")
                break
        else:
            raise CommandError("No fixture called " + fixturename + " found")

        with open(fixturefile, "r") as rawjson:
            json_data = json.loads(rawjson.read())

        new_count = 0
        changed_count = 0
        for entry in json_data:
            split_model = entry['model'].split(".")
            model = get_model(split_model[0], split_model[1])
            try:
                obj = model.objects.get(pk=entry['pk'])
                # Used to avoid saving an object that has no changes
                different = False
                for key, value in entry['fields'].items():
                    if type(value) == list:
                        if list(getattr(obj, key).values_list("pk", flat=True)) != value:
                            setattr(obj, key, value)
                            different = True
                    elif obj._meta.get_field(key).get_internal_type() == "DateField":
                        datetime_obj = datetime.strptime(value, "%Y-%m-%d")
                        if getattr(obj, key) != datetime_obj.date():
                            setattr(obj, key, value)
                            different = True
                    elif obj._meta.get_field(key).get_internal_type() == "DateTimeField":
                        datetime_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
                        # Our object doesn't have a timezone
                        origtime_without_tz = getattr(obj, key).replace(tzinfo=None)
                        if origtime_without_tz != datetime_obj:
                            setattr(obj, key, value)
                            different = True
                    elif getattr(obj, key) != value:
                        setattr(obj, key, value)
                        different = True
                if different:
                    obj.save()
                    changed_count += 1
            except model.DoesNotExist:
                model.objects.create(**entry['fields'])
                new_count += 1

        self.stdout.write(
            "Loaded fixture " + fixturename + " (" + str(new_count) + " new, " + str(changed_count) + " changed)"
        )