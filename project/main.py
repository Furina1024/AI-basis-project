import sqlite3
import re
import random
import requests
import json
from threading import Thread
import time
import sys
from input_filter import InputPreprocessor

def stream_dify_response(api_key, prompt, endpoint):
    """
    流式调用Dify API
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }  
    payload = {
        "inputs": {"location":response_location.get('city')},
        "query": prompt,
        "response_mode": "streaming", 
        "conversation_id": "",
        "user": 1,
        "files":[]
    }
    output_text.config(state='normal') 
    output_text.insert(tk.END, 'loading...')
    output_text.config(state='disabled') 
    with requests.post(endpoint, headers=headers, json=payload, stream=True) as response:
        unexcuted=True
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    data = json.loads(decoded_line[5:])
                    if 'answer' in data:
                        if unexcuted:
                            output_text.config(state='normal') 
                            last_line = output_text.index('end-1l linestart')
                            output_text.delete(last_line, 'end')  
                            output_text.config(state='disabled')   
                            unexcuted=False
                        append_text(data['answer'])

    
preprocessor = InputPreprocessor(["暴力", "毒品", "赌博"])
response_location = requests.get('https://ipapi.co/json/').json()
import tkinter as tk
from tkinter import font 
def start_thread():
    thread = Thread(target=on_button_click_submit)
    thread.start()
    button_continue.config(state="normal")
def on_button_click_submit():
    button_submit.config(state="disabled")
    user_input = entry.get()
    processed_input = preprocessor.preprocess(user_input)
    stream_dify_response("app-vw7rpTLlwM07dQLzBzaW3D2i", processed_input, "https://api.dify.ai/v1/chat-messages")

def on_button_click_continue():
    button_submit.config(state="normal")
    button_continue.config(state="disabled")
    entry.delete(0, tk.END)
    output_text.config(state='normal')  # 临时启用编辑
    output_text.insert(tk.END, '\n\n')
    output_text.config(state='disabled')  # 恢复禁用状态

def on_button_click_exit():
    root.destroy()
    sys.exit(0)   

# 创建主窗口
root = tk.Tk()
root.title("AI一枚~")
# 获取屏幕尺寸
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口尺寸
window_width = 1295
window_height = 800

# 计算居中位置
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口位置和大小
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
# 添加控件
label = tk.Label(root, text="请输入要求:",font=("Arial", 20))
label.pack()
label.place(x=450, y=50, width=400, height=50)

entry = tk.Entry(root, width=30)
entry.pack()
entry.place(x=250, y=110, width=800, height=40)

button_submit = tk.Button(root, text="提交", command=start_thread,font=("Arial", 14))
button_submit.pack()
button_submit.place(x=620, y=200, width=60, height=40)

label2 = tk.Label(root, text="输出内容:",font=("Arial", 20))
label2.pack()
label2.place(x=450, y=280, width=400, height=50)

def append_text(text):
    output_text.config(state=tk.NORMAL)  # 临时启用编辑
    output_text.insert(tk.END, text)
    output_text.see(tk.END)  # 自动滚动到最后
    output_text.config(state=tk.DISABLED)  # 恢复只读

output_text = tk.Text(root,font=("Arial", 17))
output_text.pack()
output_text.place(x=250, y=340, width=800, height=320)
output_text.config(state='disabled')

button_continue = tk.Button(root, text="继续会话", command=on_button_click_continue,font=("Arial", 14))
button_continue.pack()
button_continue.place(x=500, y=700, width=100, height=40)
button_continue.config(state="disabled")

button_exit = tk.Button(root, text="退出会话", command=on_button_click_exit,font=("Arial", 14))
button_exit.pack()
button_exit.place(x=700, y=700, width=100, height=40)

# 运行主循环
root.mainloop()
