import asyncio

from main import Main


if __name__ == "__main__":
    asyncio.Task(Main().task_is_calc())  # the task is working
    Main()._run()