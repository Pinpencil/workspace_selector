import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
import subprocess
import sys
import json
import time

# 指定你的 .code-workspace 文件夹路径（修改这里）
WORKSPACE_FOLDER = r'C:\Users\30434\Desktop\vs_workspaces'  # Windows 示例；Mac/Linux 用 '/path/to/your/workspaces'
HISTORY_FILE = os.path.join(WORKSPACE_FOLDER, '.workspace_history.json')

# ------------------ 数据与持久化 ------------------

def load_history():
    """读取历史访问时间映射 {filename: timestamp}."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 仅保留 .code-workspace 的键
                return {k: float(v) for k, v in data.items() if k.endswith('.code-workspace')}
    except Exception:
        # 历史文件损坏时忽略
        pass
    return {}

def save_history(history):
    """保存历史访问时间映射。"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        # 无写权限等情况直接忽略
        pass

def update_history(file_name):
    """更新某个工作区的最后访问时间。"""
    history = load_history()
    history[file_name] = time.time()
    save_history(history)

def load_workspaces(folder):
    """加载文件夹中的 .code-workspace 文件，返回文件名列表。"""
    if not os.path.exists(folder):
        messagebox.showerror("错误", f"文件夹不存在: {folder}")
        return []
    return [f for f in os.listdir(folder) if f.endswith('.code-workspace')]

def get_workspace_items(folder):
    """获取工作区条目列表：[{name, path, last_opened, atime, mtime}]"""
    names = load_workspaces(folder)
    history = load_history()
    items = []
    for name in names:
        path = os.path.join(folder, name)
        try:
            atime = os.path.getatime(path)
        except Exception:
            atime = 0.0
        try:
            mtime = os.path.getmtime(path)
        except Exception:
            mtime = 0.0
        items.append({
            'name': name,
            'path': path,
            'last_opened': history.get(name, 0.0),
            'atime': atime,
            'mtime': mtime,
        })
    return items

def human_time(ts):
    if not ts:
        return '—'
    try:
        # 相对时间描述
        diff = max(0, time.time() - ts)
        if diff < 60:
            return f"{int(diff)} 秒前"
        if diff < 3600:
            return f"{int(diff//60)} 分钟前"
        if diff < 86400:
            return f"{int(diff//3600)} 小时前"
        if diff < 86400*7:
            return f"{int(diff//86400)} 天前"
        # 超过一周显示日期
        return time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))
    except Exception:
        return '—'

def open_workspace(file_name):
    """打开选中的工作区文件"""
    file_path = os.path.join(WORKSPACE_FOLDER, file_name)
    try:
        # VSCode 可执行文件路径
        vscode_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Programs', 'Microsoft VS Code', 'Code.exe')
        if not os.path.exists(vscode_path):
            # 尝试全局安装路径
            vscode_path = r'C:\Program Files\Microsoft VS Code\Code.exe'

        # 更新访问历史再打开
        update_history(file_name)

        # 使用 Popen 避免阻塞界面
        subprocess.Popen([vscode_path, file_path])
        if 'root' in globals() and root:
            root.quit()  # 关闭窗口
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到 VSCode。请确保 VSCode 已安装。")
    except Exception as e:
        messagebox.showerror("错误", f"打开失败: {e}")

def create_gui():
    """创建 GUI 界面（美化 + 搜索 + 排序 + 双击/回车）"""
    global root
    root = tk.Tk()
    root.title("VSCode Workspace 选择器")
    root.geometry("640x420")
    root.minsize(560, 380)

    # 主题与样式
    style = ttk.Style()
    try:
        # 选择较现代的主题（按可用性降级）
        for theme in ('clam', 'vista', 'xpnative', 'default'):
            if theme in style.theme_names():
                style.theme_use(theme)
                break
    except Exception:
        pass

    style.configure('Header.TLabel', font=("Segoe UI", 13, 'bold'))
    style.configure('TButton', font=("Segoe UI", 10))
    style.configure('TEntry', font=("Segoe UI", 10))
    style.configure('TCombobox', font=("Segoe UI", 10))

    # 加载文件列表（若为空直接提示）
    items = get_workspace_items(WORKSPACE_FOLDER)
    if not items:
        messagebox.showinfo("提示", f"在 {WORKSPACE_FOLDER} 中未找到 .code-workspace 文件。")
        root.destroy()
        return

    # 顶部容器
    container = ttk.Frame(root, padding=12)
    container.pack(fill=tk.BOTH, expand=True)

    # Header 行
    header = ttk.Frame(container)
    header.pack(fill=tk.X)
    ttk.Label(header, text="选择工作区", style='Header.TLabel').pack(side=tk.LEFT)
    ttk.Label(header, text=f"（来自 {WORKSPACE_FOLDER}）").pack(side=tk.LEFT, padx=(6, 0))

    # 控件行：搜索 + 排序
    controls = ttk.Frame(container)
    controls.pack(fill=tk.X, pady=(10, 6))

    ttk.Label(controls, text="搜索：").pack(side=tk.LEFT)
    search_var = tk.StringVar()
    search_entry = ttk.Entry(controls, textvariable=search_var)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    ttk.Label(controls, text="  排序：").pack(side=tk.LEFT)
    sort_var = tk.StringVar(value='最近访问')
    sort_box = ttk.Combobox(controls, textvariable=sort_var, state='readonly', width=10,
                            values=['最近访问', '名称'])
    sort_box.pack(side=tk.LEFT)

    # 列表区域：Treeview + 滚动条
    list_frame = ttk.Frame(container)
    list_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('last',)
    tree = ttk.Treeview(list_frame, columns=columns, show='headings')
    tree.heading('last', text='最近访问时间')
    tree.column('last', width=160, anchor='w')

    # 第一列显示名称（用 #0 列）
    tree.configure(show='tree headings')
    tree.heading('#0', text='工作区文件')
    tree.column('#0', anchor='w')

    yscroll = ttk.Scrollbar(list_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)

    # 状态/说明行
    status_var = tk.StringVar(value='就绪')
    status = ttk.Label(container, textvariable=status_var)
    status.pack(fill=tk.X, pady=(6, 0))

    # 数据与过滤/排序
    all_items = items[:]  # 原始数据

    def apply_sort_and_filter():
        query = search_var.get().strip().lower()
        mode = sort_var.get()

        def match(item):
            if not query:
                return True
            return query in item['name'].lower()

        data = [it for it in all_items if match(it)]
        if mode == '最近访问':
            # 优先按 last_opened，其次按文件系统 atime，最后按名称
            data.sort(key=lambda it: (it.get('last_opened', 0.0) or 0.0,
                                      it.get('atime', 0.0) or 0.0,
                                      it['name'].lower()), reverse=True)
        else:
            data.sort(key=lambda it: it['name'].lower())

        # 刷新 Treeview
        tree.delete(*tree.get_children())
        for it in data:
            last = it.get('last_opened') or it.get('atime') or 0.0
            tree.insert('', tk.END, iid=it['name'], text=it['name'], values=(human_time(last),))

        status_var.set(f"共 {len(data)} 个工作区，排序：{mode}")

    def refresh():
        nonlocal all_items
        all_items = get_workspace_items(WORKSPACE_FOLDER)
        apply_sort_and_filter()

    def on_search_change(*_):
        apply_sort_and_filter()

    def on_sort_change(*_):
        apply_sort_and_filter()

    search_var.trace_add('write', on_search_change)
    sort_box.bind('<<ComboboxSelected>>', on_sort_change)

    # 交互：选择、双击、回车
    def get_selected_name():
        sel = tree.selection()
        if not sel:
            return None
        return sel[0]

    def on_open(*_):
        name = get_selected_name()
        if name:
            open_workspace(name)
        else:
            messagebox.showwarning("警告", "请先选择一个工作区。")

    def on_double_click(event):
        # 双击打开
        item_id = tree.identify_row(event.y)
        if item_id:
            tree.selection_set(item_id)
            on_open()

    def on_select_event(*_):
        name = get_selected_name()
        if not name:
            status_var.set('未选择工作区')
            return
        # 更新状态栏显示具体时间
        meta = next((it for it in all_items if it['name'] == name), None)
        if meta:
            last = meta.get('last_opened') or meta.get('atime')
            status_var.set(f"选中：{name}    最近访问：{human_time(last)}")

    tree.bind('<Double-1>', on_double_click)
    tree.bind('<<TreeviewSelect>>', on_select_event)
    root.bind('<Return>', on_open)
    root.bind('<Escape>', lambda *_: root.quit())

    # 底部按钮栏
    buttons = ttk.Frame(container)
    buttons.pack(fill=tk.X, pady=(8, 0))

    open_btn = ttk.Button(buttons, text='打开', command=on_open)
    open_btn.pack(side=tk.RIGHT)
    refresh_btn = ttk.Button(buttons, text='刷新', command=refresh)
    refresh_btn.pack(side=tk.RIGHT, padx=(0, 8))
    exit_btn = ttk.Button(buttons, text='退出', command=root.quit)
    exit_btn.pack(side=tk.LEFT)

    # 首次填充
    apply_sort_and_filter()
    # 焦点给搜索框
    search_entry.focus_set()

    # 运行 GUI
    root.mainloop()

if __name__ == "__main__":
    create_gui()