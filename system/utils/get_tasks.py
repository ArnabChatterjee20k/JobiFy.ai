from system.models.Task import Task
def get_task(id=None):
    if id:
        return Task.query.filter_by(task_id=id).all()
    return Task.query.all()