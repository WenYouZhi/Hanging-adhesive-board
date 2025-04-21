import tkinter as tk
import pyperclip
import time
import os
from tkinter import messagebox

class EnhancedClipboard:
    def __init__(self, master):
        self.master = master
        master.title("Hanging adhesive board")
        master.geometry("500x350+100+100")
        master.resizable(True, True)  # 允许窗口自由调整大小
        
        # 窗口置顶设置
        master.wm_attributes("-topmost", 1)
        self.last_clip = ""
        
        # 创建历史目录
        self.history_dir = "clip_history"
        os.makedirs(self.history_dir, exist_ok=True)
        
        # 构建界面
        self.create_widgets()
        
        # 启动剪贴板监控
        self.monitor_clipboard()

    def create_widgets(self):
        """创建界面组件"""
        # 控制按钮区域
        control_frame = tk.Frame(self.master)
        control_frame.pack(fill=tk.X, padx=5, pady=2)
        
        # 保存按钮
        save_btn = tk.Button(
            control_frame,
            text="Sava",
            command=self.save_content,
            bg="#66CCFF",
            width=12
        )
        save_btn.pack(side=tk.LEFT, padx=2)
        
        # 历史按钮
        history_btn = tk.Button(
            control_frame,
            text="History",
            command=self.show_history,
            bg="#99FF99",
            width=12
        )
        history_btn.pack(side=tk.LEFT, padx=2)
        
        # 清空按钮
        clear_btn = tk.Button(
            control_frame,
            text="Clear",
            command=self.clear_content,
            bg="#FF6666",
            width=10
        )
        clear_btn.pack(side=tk.RIGHT, padx=2)

        # 主文本区域
        self.text_area = tk.Text(
            self.master,
            wrap=tk.WORD,
            font=('微软雅黑', 10),
            bg='#FAFAD2',  # 浅黄色背景
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def monitor_clipboard(self):
        """持续监控剪贴板内容"""
        try:
            current_clip = pyperclip.paste()
            if current_clip != self.last_clip:
                self.last_clip = current_clip
                self.append_content(current_clip.strip())
        except Exception as e:
            print(f"Clipboard access exception: {e}")

        self.master.after(500, self.monitor_clipboard)

    def append_content(self, text):
        """追加新内容到文本框"""
        if text:  # 非空内容处理
            timestamp = time.strftime("\n[%H:%M:%S]\n")
            self.text_area.insert(tk.END, timestamp + text + "\n")
            self.text_area.see(tk.END)  # 自动滚动到底部

    def save_content(self):
        """保存当前内容到历史文件"""
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Save failed", "The current content is empty")
            return
        
        # 生成文件名
        filename = time.strftime("clip_%Y%m%d_%H%M%S.txt")
        filepath = os.path.join(self.history_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Successfully saved", f"The file has been saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Save failed", f"Error:\n{str(e)}")

    def show_history(self):
        """显示历史存档目录"""
        try:
            if os.name == 'nt':  # Windows系统
                os.startfile(self.history_dir)
            else:  # Mac/Linux系统
                os.system(f'open "{self.history_dir}"' if sys.platform == 'darwin' 
                          else f'xdg-open "{self.history_dir}"')
        except Exception as e:
            messagebox.showerror("Open failed", f"Unable to open directory:\n{str(e)}")

    def clear_content(self):
        """清空文本框内容"""
        self.text_area.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedClipboard(root)
    root.mainloop()
