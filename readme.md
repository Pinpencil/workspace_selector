# VSCode Workspace 选择器

## 简介
快速启动和管理 VS Code 工作区文件（.code-workspace）的图形化工具。  
自动记录并按最近访问时间排序，支持搜索和快捷键操作。

## 文件说明
- `vs_run.vbs` - 启动器（双击运行，无控制台窗口）
- `vs_run.py` - 主程序（Tkinter GUI）
- `.workspace_history.json` - 访问历史记录（自动生成）
- `*.code-workspace` - VS Code 工作区配置文件

## 快速开始
1. 双击 `vs_run.vbs` 启动程序
2. 在列表中选择工作区（或使用搜索框快速查找）
3. 双击/按回车键打开，或点击"打开"按钮

## 如何创建工作区文件
在 VS Code 中保存工作区到此目录：

1. 打开 VS Code，添加需要的文件夹  
   菜单: 文件 → 将文件夹添加到工作区...

2. 保存工作区配置文件  
   菜单: 文件 → 将工作区另存为...  
   保存位置: `C:\Users\30434\Desktop\vs_workspaces\`  
   文件名: 输入项目名称（如 `my_project.code-workspace`）

3. 完成后，该工作区会自动出现在启动器列表中

## 主要功能
- ✓ 智能排序：按最近访问时间或名称排序
- ✓ 实时搜索：快速过滤工作区列表
- ✓ 访问记录：自动保存打开历史，下次优先显示
- ✓ 友好交互：支持双击、Enter 打开，Esc 退出
- ✓ 无控制台：通过 VBS 启动器隐藏命令行窗口

## 键盘快捷键
- **Enter** - 打开选中的工作区
- **Esc** - 退出程序
- **双击列表项** - 快速打开

## 配置
### 修改工作区文件夹路径
1. 用文本编辑器打开 `vs_run.py`
2. 找到第 11 行：  
   ```python
   WORKSPACE_FOLDER = r'C:\Users\30434\Desktop\vs_workspaces'
   ```
3. 修改为你的实际路径，例如：  
   ```python
   WORKSPACE_FOLDER = r'D:\MyWorkspaces'
   ```
4. 保存文件即可

### 修改 VS Code 安装路径（如果自动检测失败）
1. 打开 `vs_run.py`
2. 找到第 50-53 行左右的 `vscode_path` 设置
3. 将路径改为你的 VS Code 安装位置，例如：  
   ```python
   vscode_path = r'D:\Program Files\VSCode\Code.exe'
   ```
   
4. 修改后需重新启动程序生效

## 依赖环境
- Python 3.x（需安装 tkinter，通常已内置）
- VS Code（会自动检测常见安装路径）
- Windows 系统（VBS 启动器仅支持 Windows）

## 故障排查
### 双击 vbs 无反应
- 检查 Python 是否已安装并添加到 PATH
- 在命令行测试：`python --version`
- 尝试直接运行：`python vs_run.py`

### 提示"未找到 VSCode"
- 检查 VS Code 是否已安装
- 手动配置路径（见上方【配置】章节）

### 列表为空/未显示工作区文件
- 确认 `.code-workspace` 文件在正确目录下
- 检查 `WORKSPACE_FOLDER` 路径配置是否正确
- 点击"刷新"按钮重新加载

### 删除访问历史记录
- 删除 `.workspace_history.json` 文件即可
- 或手动编辑该 JSON 文件移除特定条目

## 版本
v1.0

## 日期
2025-10-29