from backend_util.src.errorcode import ErrorCode
from SingleLog.log import Logger

if __name__ == '__main__':
    logger = Logger('demo logger', Logger.INFO)

    logger.show(
        Logger.INFO,
        'demo log')

    logger.show(
        Logger.INFO,
        'show value',
        12)

    logger.show(
        Logger.INFO,
        'Error code',
        ErrorCode.Success)
