import sys
import time
import threading

from SingleLog.log import Logger

from backend_util.src.console import Console
from backend_util.src.config import Config
from backend_util.src.event import EventConsole
from backend_util.src.dynamic_data import DynamicData
from backend_util.src.websocketserver import WsServer
from backend_util.src.command import Command

import version

logger = Logger('server', Logger.INFO)
logger.show(Logger.INFO, 'uPtt server', version.v)

logger.show(
    Logger.INFO,
    '初始化',
    '啟動')
console_obj = Console()
console_obj.role = Console.role_server

config_obj = Config(console_obj)
console_obj.config = config_obj

logger.show(
    Logger.INFO,
    '執行模式',
    console_obj.run_mode)

event_console = EventConsole(console_obj)
console_obj.event = event_console

dynamic_data_obj = DynamicData(console_obj)
if not dynamic_data_obj.update_state:
    logger.show(
        Logger.INFO,
        'Update dynamic data error')
    sys.exit()
console_obj.dynamic_data = dynamic_data_obj

comm_obj = Command(console_obj)
console_obj.command = comm_obj

logger.show(
    Logger.INFO,
    '初始化',
    '完成')

run_server = True


def event_close(p):
    global run_server
    run_server = False


ws_server = WsServer(console_obj)

event_console.register(
    EventConsole.key_close,
    ws_server.stop)

event_console.register(
    EventConsole.key_close,
    event_close)

ws_server.start()

if ws_server.start_error:
    logger.show(
        Logger.INFO,
        'websocket client-server startup error')
    event_console.execute(EventConsole.key_close)
else:

    logger.show(
        Logger.INFO,
        '初始化',
        '完成')

    while run_server:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            event_console.execute(EventConsole.key_close)
            break

logger.show(
    Logger.INFO,
    '執行最終終止程序')

running = threading.Event()
running.set()
running.clear()

logger.show(
    Logger.INFO,
    '最終終止程序全數完成')
