#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import sys
import csv
from collections import namedtuple

# 个税起征点常量
INCOME_TAX_START_POINT = 5000

# 税率表条目类,该类由 namedtuple 动态创建,代表一个命名元组
IncomeLookupItem = namedtuple(
    'IncomeLookupItem',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

# 税率表,里面的元素类型为前面创建的 IncomeLookupItem
INCOME_TAX_QUICK_LOOKUP_TABLE = [
	IncomeLookupItem(80000, 0.45, 15160),
	IncomeLookupItem(55000, 0.35, 7160),
	IncomeLookupItem(35000, 0.30, 4410),
	IncomeLookupItem(25000, 0.25, 2660),
	IncomeLookupItem(12000, 0.2, 1410),
	IncomeLookupItem(3000, 0.1, 210),
	IncomeLookupItem(0, 0.03, 0)
]

# 类:处理命令行参数
class Args:

	def __init__(self):
		self.args = sys.argv[1:]

	def _value_after_option(self, option):
		try:
			index = self.args.index(option)
			return self.args[index + 1]
		except(ValueError, IndexError):
			print('Parameter Error')
			exit()

	@property
	def config_path(self):
		return self._value_after_option('-c')

	@property
	def userdata_path(self):
		return self._value_after_option('-d')

	@property
	def exportfile_path(self):
		return self._value_after_option('-o')


# 创建全局参数对象供后续使用
args = Args()


# 类:配置文件
class Config:

	def __init__(self):
		self.config = self._read_config()

	# 配置文件读取内部函数
	def _read_config(self):
		config = {}
		with open(args.config_path) as f:
			# 依次读取配置文件每行数据并解析得到K&V
			for line in f.readlines():
				key, val = line.strip().split('=')
				try:
					config[key.strip()] = float(val.strip())
				except ValueError:
					print('Parameter Error')
					exit()

	def _get_config(self, key):
		# 获得配置项对应的值
		try:
			return self.config[key]
		except KeyError:
			print('Parameter Error')
			exit()

	@property
	def social_insurance_baseline_low(self):
		# 返回社保基数地板线
		return self._get_config('JiShuL')

	@property
	def social_insurance_baseline_high(self):
		# 返回社保基数屋顶线
		return self._get_config('JiShuH')

	@property
	def social_insurance_total_rate(self):
		# 返回社保总费率
		return sum([
			self._get_config('YangLao'),
			self._get_config('YiLiao'),
			self._get_config('ShiYe'),
			self._get_config('GongShang'),
			self._get_config('ShengYu'),
			self._get_config('GongJiJin')
		])


# 创建全局 config 供使用
config = Config()


# 类:用户数据
class UserData:

	def __init__(self):
		self.userdata = self._read_users_data()

	# 用户数据读取
	def _read_users_data(self):
		userdata = []
		with open(args.userdata_path) as f:
			for line in f.readlines():
				employee_id, income_string = line.strip().split(',')
				try:
					income = int(income_string)
				except ValueError:
					print('Parameter Error')
					exit()
				userdata.append((employee_id, income))
		return userdata

	def get_userdata(self):
		return self.userdata


# 类:税后工资计算
class IncomeCalculator:

	def __init__(self, userdata):
		self.userdata = userdata

	# 计算社保金额
	@classmethod
	def calc_social_insurance_money(cls, income):
		if income < config.social_insurance_baseline_low:
			return config.social_insurance_baseline_low * config.social_insurance_total_rate
		elif income > config.social_insurance_baseline_high:
			return config.social_insurance_baseline_high * config.social_insurance_total_rate
		else:
			return income * config.social_insurance_total_rate

	@classmethod
	def calc_income_tax_and_remain(cls, income):
		# 社保金额
		social_insurance_money = cls.calc_social_insurance_money(income)
		# 应纳税金额
		taxable_part = income - social_insurance_money - INCOME_TAX_START_POINT
		# 从高到低判断落入的税率区间
		for item in INCOME_TAX_QUICK_LOOKUP_TABLE:
			if taxable_part > item.start_point:
				tax = taxable_part * item.tax_rate - item.quick_subtractor
				return '{:.2f}'.format(tax), '{:.2f}'.format(social_insurance_money - tax)
		return '0.00', '{:.2f}'.format(income - social_insurance_money)

	# 计算每位员工的税后工资
	def calc_for_all_userdata(self):
		result = []
		# 循环计算每个员工的税后工资
		for id, income in self.userdata.get_userdata():
			# 社保金额
			social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
			# 税后工资
			tax, remain = self.calc_income_tax_and_remain(income)
			result.append([id, income, social_insurance_money, tax, remain])
		return result

	# 输出 CSV 文件
	def export_to_csv(self):
		data = self.calc_for_all_userdata()
		with open(args.exportfile_path, 'w', newline='') as f:
			csv.writer(f).writerows(data)


if __name__ == '__main__':
	# 创建税后工资计算器
	calculator = IncomeLookupItem(UserData())
	calculator.export_to_csv()