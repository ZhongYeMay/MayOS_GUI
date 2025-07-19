import tkinter as tk
from tkinter import messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("计算器")
        self.geometry("320x420")
        self.resizable(False, False)
        self.configure(bg="#f0f0f0")
        self.expression = ""
        self.create_widgets()
        self.bind_keys()

    def bind_keys(self):
        self.bind('<Key>', self.on_key_press)
        self.bind('<Return>', lambda e: self.calculate())
        self.bind('<Escape>', lambda e: self.clear())

    def on_key_press(self, event):
        char = event.char
        if char in '0123456789.+-*/':
            self.on_button_click(char)
        elif char == '\r':  # 回车
            self.calculate()
        elif char == '\x1b':  # Esc
            self.clear()

    def create_widgets(self):
        # 顶部标题标签，采用MD3风格
        title_label = tk.Label(
            self,
            text="MayOS GUI 计算器 v1.0",
            font=("Google Sans", 16, "bold"),
            bg="#F5F5F5",
            fg="#1A1A1A",
            pady=12
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(10,0))

        # 显示框采用MD3风格
        self.display = tk.Entry(
            self,
            font=("Google Sans", 24),
            bd=0,
            relief=tk.FLAT,
            justify='right',
            bg="#FFFFFF",
            fg="#1A1A1A",
            highlightthickness=2,
            highlightbackground="#E0E0E0",
            highlightcolor="#4285F4"
        )
        self.display.grid(row=1, column=0, columnspan=4, padx=16, pady=16, sticky="nsew")

        btn_texts = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
            ["=",],
        ]
        md3_colors = {
            'default_bg': '#E8EAED',
            'default_fg': '#1A1A1A',
            'accent_bg': '#4285F4',
            'accent_fg': '#FFFFFF',
            'clear_bg': '#F44336',
            'clear_fg': '#FFFFFF',
        }
        for r, row in enumerate(btn_texts):
            for c, text in enumerate(row):
                if text == "=":
                    btn = tk.Button(
                        self,
                        text=text,
                        font=("Google Sans", 20, "bold"),
                        bg=md3_colors['accent_bg'],
                        fg=md3_colors['accent_fg'],
                        bd=0,
                        relief=tk.FLAT,
                        activebackground="#3367D6",
                        activeforeground="#FFFFFF",
                        highlightthickness=0,
                        cursor="hand2",
                        command=self.calculate
                    )
                    btn.grid(row=r+2, column=0, columnspan=4, sticky="nsew", padx=16, pady=8, ipadx=0, ipady=12)
                else:
                    bg = md3_colors['default_bg']
                    fg = md3_colors['default_fg']
                    if text == "C":
                        bg = md3_colors['clear_bg']
                        fg = md3_colors['clear_fg']
                    btn = tk.Button(
                        self,
                        text=text,
                        font=("Google Sans", 20),
                        bg=bg,
                        fg=fg,
                        bd=0,
                        relief=tk.FLAT,
                        activebackground="#DADCE0",
                        activeforeground="#1A1A1A",
                        highlightthickness=0,
                        cursor="hand2",
                        command=lambda t=text: self.on_button_click(t)
                    )
                    btn.grid(row=r+2, column=c, sticky="nsew", padx=8, pady=8, ipadx=0, ipady=12)

        for i in range(5):
            self.grid_rowconfigure(i+2, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == "C":
            self.clear()
        else:
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)

    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = result
        except Exception:
            messagebox.showerror("错误", "表达式无效！")
            self.clear()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()