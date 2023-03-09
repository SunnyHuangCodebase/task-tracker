from asgiref.sync import sync_to_async
from django.db.models import AutoField, BooleanField, Model, TextField


class Task(Model):
    id: int = AutoField(primary_key=True)
    name: str = TextField()
    complete: bool = BooleanField(default=False)

    class Meta:
        db_table = 'task'

    @classmethod
    async def a_get(cls, task_id: int):
        return await sync_to_async(Task.objects.get)(id=task_id)

    @classmethod
    async def a_toggle_complete(cls, task_id: int):
        self = await cls.a_get(task_id)
        self.complete = not self.complete
        await sync_to_async(self.save)()

    @classmethod
    async def a_delete(cls, task_id: int):
        self = await cls.a_get(task_id)
        await sync_to_async(self.delete)()

    @classmethod
    async def a_delete_all(cls):
        await sync_to_async(cls.objects.all().delete)()

    @classmethod
    async def a_create(cls, name):
        task = Task(name=name)
        await sync_to_async(task.save)()
        return task
