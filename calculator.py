#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys,csv

# 类:处理配置文件
class Config(object):

	def __init__(self, configfile):
		self._file = configfile
		self._config = {}
		pass

	# 读取文件内容
	def get_config(self):
		with open(self._file) as f:
			print(csv.reader(f))
			# for k in


# 类:处理员工数据
class UserData(object):

	def __init__(self, userdatafile):
		self.userdata = {}
		pass

	# 计算
	def calculator(self):
		pass

	# 输出到文件
	def dumptofile(self):
		pass


if __name__ == '__main__':
	argv = sys.argv[1:]	# 获取交互行参数
	if len(argv) == 6:

		configdirt = Config(argv[argv.index('-c')+1])
		configdirt.get_config()

	else:
		raise 'Paramters Error'
