from django.core.management.base import BaseCommand
from time import strftime, localtime

class Command(BaseCommand):
    help = '这是第二个command测试指令'

    # 为handle中添加参数解析，
    def add_arguments(self, parser):
        parser.add_argument(
            '-p', # 设置参数的时候  前边携带
            '--param',
            action='store',
            dest='param',  # 自定义传入的参数键名ss
            default='close',  # 默认的键值
            help='name of author.',
        )

    def handle(self, *args, **options):
        # print("mycommand2----开始")
        '''
        添加你需要功能，（访问数据库，判断有效性等等）
        ...
        '''
        # 例如
        if options['param']:
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()), end='')
            print(": mycommand2传入的参数为", options['param'])
        # print("mycommand2----结束")


