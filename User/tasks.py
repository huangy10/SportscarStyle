from SportscarStyle.celery import app


@app.task()
def image_resize(instance, field_name, target_size):
    pass
