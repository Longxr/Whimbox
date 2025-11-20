from whimbox.task.task_template import TaskTemplate, register_step
import time
from whimbox.common.logger import logger

class TestTask(TaskTemplate):
    def __init__(self):
        super().__init__("test_task")
        self.count = 0

    @register_step("测试步骤")
    def step1(self):
        while not self.need_stop():
            logger.info(f"测试步骤，第{self.count}次")
            self.count += 1
            time.sleep(5)