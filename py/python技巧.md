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
