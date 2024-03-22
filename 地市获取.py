import pandas as pd
import requests
from bs4 import BeautifulSoup


# 加载上传的Excel文件
file_path = '/path/to/your/file.xlsx'  # 替换为实际文件路径
data = pd.read_excel(file_path)

# 移除名称中的前后空白字符
data['  单位名称'] = data['  单位名称'].str.strip()

# 为省、市、区创建新列
data['Province'] = None
data['City'] = None
data['District'] = None

# 初始化省和市变量
province, city = None, None

# 遍历数据，根据行政区划代码进行分类
for index, row in data.iterrows():
    if pd.notnull(row['行政区划代码']):  # 检查代码是否非NaN
        code = str(int(row['行政区划代码']))
        name = row['  单位名称']
        if code.endswith('0000'):  # 省级
            province = name
            city = None  # 遇到新省份时重置城市
        elif code.endswith('00') and not code.endswith('0000'):  # 市级
            city = name
        else:  # 区级
            district = name
            data.at[index, 'Province'] = province
            data.at[index, 'City'] = city if city is not None else province  # 某些地区可能没有市级
            data.at[index, 'District'] = district

# 过滤出区级非空的行（即只保留最具体的行政级别）
organized_data = data.dropna(subset=['District'])

# 选择省、市、区的列
organized_data = organized_data[['Province', 'City', 'District']]

# 将整理好的数据保存到新的Excel文件
output_path = '/path/to/your/output_file.xlsx'  # 替换为期望的输出文件路径
organized_data.to_excel(output_path, index=False)
