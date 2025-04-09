import pandas as pd

# 读取原始Excel文件
file_path = '续聘教师评教.xlsx'  # 请替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 获取所有教师的姓名列表
teachers = df['教师姓名'].unique()

# 循环遍历每个教师的姓名，过滤出该教师的数据并保存为新的Excel文件
for teacher in teachers:
    teacher_data = df[df['教师姓名'] == teacher]
    
    # 生成每个教师对应的文件名
    output_file = f'{teacher}.xlsx'  # 可以根据需要调整命名规则
    
    # 保存该教师的数据到新的Excel文件
    teacher_data.to_excel(output_file, index=False)

    print(f"保存文件: {output_file}")
