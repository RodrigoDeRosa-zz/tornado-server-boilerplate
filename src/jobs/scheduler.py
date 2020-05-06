from datetime import datetime, timedelta

from tornado.ioloop import IOLoop

from src.jobs.concurrent_example_job import ConcurrentExampleJob
from src.jobs.example_job import ExampleJob


class Scheduler:

    @classmethod
    def example_set_up(cls):
        """ Configure jobs to be run on scheduled times. """
        cls.run_in_millis(ExampleJob.run, millis=100)
        cls.run_in_millis(ConcurrentExampleJob.run, millis=0)
        # cls.run_every_millis(ExampleJob.run, delta_millis=500)
        # cls.schedule_for_time(ExampleJob.run)  # Run at midnight

    @classmethod
    def run_in_millis(cls, coroutine, millis=0):
        """ Set coroutine to run given milliseconds from now. """
        IOLoop.current().add_timeout(timedelta(milliseconds=millis), coroutine)

    @classmethod
    def run_every_millis(cls, coroutine, delta_millis=0):
        """ Schedule a task to be run every `delta_millis` milliseconds. """
        cls.schedule_job(
            timedelta(milliseconds=delta_millis),
            cls.run_every_millis,
            coroutine,
            **{'delta_millis': delta_millis}
        )

    @classmethod
    def schedule_for_time(cls, coroutine, hour=0, minute=0, second=0):
        """ Schedules a task to be executed at the given cron. """
        # Calculate the remaining time until next execution
        scheduled_time = datetime.now().replace(hour=hour, minute=minute, second=second)
        current_time = datetime.now()
        if scheduled_time < current_time: scheduled_time += timedelta(days=1)
        delta = scheduled_time - current_time
        # Set for running indefinitely
        cls.schedule_job(
            delta,
            cls.schedule_for_time,
            coroutine,
            **{'hour': hour, 'minute': minute, 'second': second}
        )

    @classmethod
    def schedule_job(cls, execution_delta, delta_calculator, coroutine, **kwargs):
        """ This method schedules a job to be run indefinitely with a fixed delta. """
        async def wrapped_function():
            await coroutine()
            delta_calculator(coroutine, **kwargs)
        IOLoop.current().add_timeout(execution_delta, wrapped_function)
