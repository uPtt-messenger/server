from single_log.log import Logger

from backend_util.src.event import EventConsole
from backend_util.src.errorcode import ErrorCode
from backend_util.src.msg import Msg
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

        self.console = console_obj

        self.logger = Logger('Command', self.console.config.log_level, handler=self.console.config.log_handler)

    def check_token(self, msg):
        if msg is None:
            return False
        if Msg.key_token not in msg.data:
            return False

        current_token = msg.data[Msg.key_token]

        return self.console.login_token == current_token

    def analyze(self, recv_msg: Msg):

        opt = recv_msg.get(Msg.key_opt)
        if opt == 'echo':
            current_res_msg = Msg(
                operate=opt,
                code=ErrorCode.Success,
                msg=recv_msg.get(Msg.key_msg)
            )
            self.push(current_res_msg)
        else:
            current_res_msg = Msg(
                operate=opt,
                code=ErrorCode.Unsupported,
                msg='Unsupported')
            self.push(current_res_msg)

    def push(self, push_msg):
        self.push_msg.append(push_msg.__str__())
