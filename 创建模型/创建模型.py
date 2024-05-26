import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_and_run_exe():
    # 打开exe文件选择对话框
    exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    if not exe_path:
        print("未选择exe文件")
        return

    # 打开文件夹选择对话框
    folder_path = filedialog.askdirectory()
    if not folder_path:
        print("未选择文件夹")
        return

    # 使用subprocess运行exe文件并传递文件夹路径作为参数
    try:
        subprocess.run([exe_path, folder_path], check=True)
        print("程序运行成功")
        messagebox.showinfo("信息", "程序运行成功")
    except subprocess.CalledProcessError as e:
        print(f"运行程序时出错: {e}")
        messagebox.showerror("错误", f"运行程序时出错: {e}")

# 创建一个简单的GUI
root = tk.Tk()
root.title("选择exe文件并运行")

select_button = tk.Button(root, text="选择exe文件并运行", command=select_and_run_exe)
select_button.pack(pady=20)

root.mainloop()
