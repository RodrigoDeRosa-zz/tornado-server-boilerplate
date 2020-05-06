from asyncio import sleep

from src.utils.concurrency.single_process_coroutine import single_process_coroutine
from src.utils.logging.logger import Logger


class ConcurrentExampleJob:

    @classmethod
    @single_process_coroutine('concurrent-job-lock')
    async def run(cls):
        cls.get_logger().info(f'Running concurrent example scheduled job. [sleep a second]')
        await sleep(1)
        cls.get_logger().info(f'Finished concurrent example scheduled job.')

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
