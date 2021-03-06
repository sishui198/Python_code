from __future__ import absolute_import, unicode_literals
from .celery import app
from celery.schedules import crontab


##########通过函数创建定时任务##########

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    return x + y


##########通过配置文件创建定时任务##########

app.conf.beat_schedule = {
    # Executes tasks.add every 30 seconds
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}


app.conf.beat_schedule = {
    # Executes tasks.add every Monday morning at 7:30 a.m
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}

app.conf.timezone = 'UTC'