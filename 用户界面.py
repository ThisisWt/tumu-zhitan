import tkinter as tk
from tkinter import messagebox

# 定义数据处理函数
def process_data(input_data):
    # 在这里进行数据处理，这里只是一个示例，将输入数据加倍返回
    return input_data * 2

# 定义按钮点击事件
def button_click():
    input_text = entry.get()  # 获取输入框中的文本
    try:
        input_number = float(input_text)  # 将输入文本转换为浮点数
        result = process_data(input_number)  # 调用数据处理函数
        messagebox.showinfo("结果", f"处理后的结果为: {result}")  # 显示处理结果
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字！")

# 创建主窗口
root = tk.Tk()
root.title("简单数据处理程序")

# 创建标签和输入框
label = tk.Label(root, text="请输入一个数字:")
label.pack()
entry = tk.Entry(root)
entry.pack()

# 创建按钮
button = tk.Button(root, text="处理", command=button_click)
button.pack()

# 运行主循环
root.mainloop()
