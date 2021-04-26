import asyncio

from main import Main


if __name__ == "__main__":
    asyncio.Task(Main().task_reestr())
    Main()._run()