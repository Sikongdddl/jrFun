import pandas as pd

# 假设你的数据已经在一个CSV文件中，或者你可以直接创建一个DataFrame

file_path = "2.xlsx"
df = pd.read_excel(file_path)

# 计算每位老师的开课学院排名百分比和学科大类排名百分比的平均值
avg_values = df.groupby('教师姓名')[['开课学院排名百分比', '学科大类排名百分比']].mean().reset_index()

# 将平均值放在每位老师的第一个条目的“学科大类排名百分比”这一列的下两列
for index, row in avg_values.iterrows():
    name = row['教师姓名']
    avg_college_rank = row['开课学院排名百分比']
    avg_major_rank = row['学科大类排名百分比']
    
    # 找到该老师的第一个条目
    first_index = df[df['教师姓名'] == name].index[0]
    
    # 将平均值放在下两列
    df.at[first_index, '开课学院排名平均值'] = avg_college_rank
    df.at[first_index, '学科大类排名平均值'] = avg_major_rank

output_file_path = 'processed2.xlsx'
df.to_excel(output_file_path)
