import threading
import random

from SingleLog.log import Logger

from backend_util.src.event import EventConsole
from backend_util.src.errorcode import ErrorCode
from backend_util.src.msg import Msg
from backend_util.src import util
from tag import Tag


class Command:
    def __init__(self, console_obj):
        self.login = False
        self.logout = False

        self.push_msg = []

        self.login_id = None
        self.login_password = None
        self.logout = False
        self.close = False
        self.send_waterball_id = None
        self.send_waterball_content = None
        self.add_friend_id = None
        self.ptt_bot_lock = threading.Lock()

        self.console = console_obj

        self.logger = Logger('Command', self.console.config.log_level, handler=self.console.config.log_handler)

    def check_token(self, msg):
        if msg is None:
            return False
        if Msg.key_token not in msg.data:
            return False

        current_token = msg.data[Msg.key_token]

        return self.console.login_token == current_token

    def _check_parameter(self, opt, p):
        if p is not None:
            return True

        current_res_msg = Msg(
            operate=opt,
            code=ErrorCode.ErrorParameter)

        self.push(current_res_msg)

        return False

    def analyze(self, recv_msg: Msg):

        self.logger.show(Logger.INFO, '訊息', recv_msg)

        opt = recv_msg.get(Msg.key_opt)
        self.logger.show(Logger.INFO, 'operation', opt)
        if opt == 'echo':
            current_res_msg = Msg(
                operate=opt,
                code=ErrorCode.Success,
                msg=recv_msg.get(Msg.key_msg))
            self.push(current_res_msg)
        elif opt == 'getToken':
            current_ptt_id = recv_msg.get(Msg.key_ptt_id)
            if not self._check_parameter(opt, current_ptt_id):
                return
            self.logger.show(Logger.INFO, 'ptt_id', current_ptt_id)
            current_token = util.generate_token()

            self.logger.show(Logger.INFO, 'token', current_token)

            self.ptt_bot_lock.acquire()



            self.ptt_bot_lock.release()

        else:
            current_res_msg = Msg(
                operate=opt,
                code=ErrorCode.Unsupported,
                msg='Unsupported')
            self.push(current_res_msg)

    def push(self, push_msg):
        self.push_msg.append(push_msg.__str__())
