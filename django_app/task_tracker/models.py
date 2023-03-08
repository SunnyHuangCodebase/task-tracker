from typing import Any

from django.db.models import AutoField, BooleanField, Model, TextField


class Task(Model):
    id: int = AutoField(primary_key=True)
    name: str = TextField()
    complete: bool = BooleanField(default=False)

    class Meta:
        db_table = 'task'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.save()

    def toggle_complete(self):
        self.complete = not self.complete
        self.save()

    @classmethod
    def delete_all(cls):
        cls.objects.all().delete()
