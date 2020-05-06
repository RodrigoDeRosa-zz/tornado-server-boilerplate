from asyncio import sleep

from src.utils.logging.logger import Logger


class ExampleJob:

    @classmethod
    async def run(cls):
        cls.get_logger().info(f'Running example scheduled job. [sleep a second]')
        await sleep(1)
        cls.get_logger().info(f'Finished example scheduled job.')

    @classmethod
    def get_logger(cls):
        return Logger(cls.__name__)
