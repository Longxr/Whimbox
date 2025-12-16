from whimbox.common.cvars import LAUNCHER_PROCESS_NAME, PROCESS_NAME
from whimbox.common.handle_lib import ProcessHandler
from whimbox.common.logger import logger
from whimbox.config.config import global_config
from whimbox.task.task_template import *


class CloseGameTask(TaskTemplate):
    """关闭游戏和启动器的任务"""
    
    def __init__(self):
        super().__init__("close_game_task")
        self.close_option = global_config.get("Game", "close_option_after_onedragon", "无操作")
    
    @register_step("检查关闭选项")
    def step1(self):
        """检查配置，决定执行哪种关闭操作"""
        if self.close_option == "关闭游戏":
            self.log_to_gui("配置为：关闭游戏")
            return "step2"
        else:
            self.log_to_gui("配置为：无操作，保持游戏运行")
            self.update_task_result(status=STATE_TYPE_SUCCESS, message="保持游戏运行")
            return STEP_NAME_FINISH
    
    @register_step("关闭游戏和启动器进程")
    def step2(self):
        """关闭游戏和启动器进程"""
        # 关闭游戏进程
        self.log_to_gui("正在关闭游戏进程...")
        game_handler = ProcessHandler(process_name=PROCESS_NAME)
        
        if game_handler.terminate_process():
            self.log_to_gui("游戏进程已关闭")
        else:
            logger.warning("未找到游戏进程或关闭失败")
        
        # 关闭启动器进程
        self.log_to_gui("正在关闭启动器进程...")
        launcher_handler = ProcessHandler(process_name=LAUNCHER_PROCESS_NAME)
        
        if launcher_handler.terminate_process():
            self.log_to_gui("启动器进程已关闭")
            self.update_task_result(status=STATE_TYPE_SUCCESS, message="游戏和启动器进程已关闭")
        else:
            logger.warning("未找到启动器进程或关闭失败")
            self.update_task_result(status=STATE_TYPE_SUCCESS, message="游戏已关闭，启动器未找到")

