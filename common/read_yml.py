import yaml
from main import DIR, Environ

"""
yaml文件特性
1.读取结果是个字典对象
2.文件操作时不会影响原有yml文件数据
3.编写文件时有规范要求，如果编写有误会抛异常
"""


class ReadYaml:
    """读取环境层的配置"""

    @staticmethod
    def env_yaml():
        with open((DIR + '/env_config/' + Environ) + '/config.yml', "r", encoding="utf-8") as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def api_yaml(group_name):
        """
        接口数据驱动的读取方式
        :param group_name:如果配置存储没有嵌套目录结构，只需要传递包名，比方说 api_yaml('notes'),如果有嵌套的目录结构，
        参考 api_yaml('notes/notesvrSetNotegroup')
        :return:
        """
        with open((DIR + r"/data") + "/" + group_name + '/api_data.yml', "r", encoding="utf-8") as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def common_yaml(filename):
        with open(filename, "r", encoding="utf-8") as f:
            # 调用load方法加载文件流
            return yaml.load(f, Loader=yaml.FullLoader)


if __name__ == '__main__':
    RY = ReadYaml()
    api_data = RY.api_yaml('note_groups/notesvrSetNotegroup')
    print(api_data)
