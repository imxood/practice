# python3 笔记

len(obj), 计算字符串, 列表, 元组, 字典等类型的长度

type(obj), 判断对象的类型

isinstance(obj, class_name), 判断是否是指定类型的变量

## 字符串常见用法

## 元组

## 字典

## 列表

## json

## shutil

    shutil.copytree(src, dst, symlinks=False), 复制目录
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*~', '*.pyc')), 忽略指定类型的文件

## 搜索包是否被安装

方法1:

    try:
        from pip._internal.utils.misc import get_installed_distributions
    except ImportError:  # pip<10
        from pip import get_installed_distributions

方法2:

    import pkg_resources

    dists = [d for d in pkg_resources.working_set]

## python 版本

    os.name, 当前操作系统的类型，当前只注册了3个值：posix , nt , java, (linux/windows/java虚拟机)

    sys.platform, "linux"

    platform.system(), 系统名称('Linux', 'Windows', or 'Java'): 'Linux', 如果无法确定就返回None

    platform.platform(), 'Linux-4.15.0-55-generic-x86_64-with-Ubuntu-16.04-xenial'

    platform.version(), Ubuntu中, 获取操作系统版本号: '#60~16.04.2-Ubuntu SMP Thu Jul 4 09:03:09 UTC 2019'

    platform.architecture(), Ubuntu中: ('64bit', 'ELF')

    platform.machine(), 'x86_64'

    platform.node(), '主机名', 计算机的网络名称

    platform.processor(), 'x86_64', 计算机处理器信息

    platform.uname(), 包含上面所有的信息汇总
