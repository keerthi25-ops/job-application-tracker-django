from datetime import datetime
from pathlib import Path
import shutil

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a timestamped backup of the local SQLite database and export app data as JSON."

    def handle(self, *args, **options):
        backup_root = Path(settings.BASE_DIR) / "backups"
        backup_root.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        db_settings = settings.DATABASES["default"]
        db_engine = db_settings.get("ENGINE", "")

        if db_engine != "django.db.backends.sqlite3":
            self.stdout.write(
                self.style.WARNING(
                    "This backup command currently copies the SQLite database file only."
                )
            )

        db_path = Path(db_settings["NAME"])
        if db_path.exists():
            db_backup_path = backup_root / f"db_backup_{timestamp}.sqlite3"
            shutil.copy2(db_path, db_backup_path)
            self.stdout.write(self.style.SUCCESS(f"Database backup created: {db_backup_path}"))
        else:
            self.stdout.write(self.style.WARNING(f"Database file not found: {db_path}"))

        json_backup_path = backup_root / f"data_backup_{timestamp}.json"
        with json_backup_path.open("w", encoding="utf-8") as output_file:
            management.call_command(
                "dumpdata",
                "auth.user",
                "TRACKER",
                indent=2,
                stdout=output_file,
            )

        self.stdout.write(self.style.SUCCESS(f"JSON export created: {json_backup_path}"))
