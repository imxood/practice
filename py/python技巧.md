# python技巧

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

os.name		# 当前操作系统的类型，当前只注册了3个值：posix , nt , java, (linux/windows/java虚拟机)

sys.platform

platform.system()	# Returns the system/OS name, ('Linux', 'Windows', or 'Java').
					# An empty string is returned if the value cannot be determined.

platform.platform()     #获取操作系统名称及版本号

platform.version()        #获取操作系统版本号

platform.architecture()    #获取操作系统的位数    

platform.machine()     #计算机类型      

platform.node()          #计算机的网络名称' 

platform.processor()    #计算机处理器信息'   

platform.uname()        #包含上面所有的信息汇总


## vscode 中python multiprocessing

	import multiprocessing
	multiprocessing.set_start_method('spawn', True)
