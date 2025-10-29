================================
  VSCode Workspace 选择器
================================

【简介】
快速启动和管理 VS Code 工作区文件（.code-workspace）的图形化工具。
自动记录并按最近访问时间排序，支持搜索和快捷键操作。


【文件说明】
  vs_run.vbs          - 启动器（双击运行，无控制台窗口）
  vs_run.py           - 主程序（Tkinter GUI）
  .workspace_history.json - 访问历史记录（自动生成）
  *.code-workspace    - VS Code 工作区配置文件


【快速开始】
  1. 双击 vs_run.vbs 启动程序
  2. 在列表中选择工作区（或使用搜索框快速查找）
  3. 双击/按回车键打开，或点击"打开"按钮


【主要功能】
  ✓ 智能排序：按最近访问时间或名称排序
  ✓ 实时搜索：快速过滤工作区列表
  ✓ 访问记录：自动保存打开历史，下次优先显示
  ✓ 友好交互：支持双击、Enter 打开，Esc 退出
  ✓ 无控制台：通过 VBS 启动器隐藏命令行窗口


【键盘快捷键】
  Enter       - 打开选中的工作区
  Esc         - 退出程序
  双击列表项   - 快速打开


【配置】
  若需修改工作区文件夹路径，编辑 vs_run.py 第 11 行：
  WORKSPACE_FOLDER = r'C:\Users\30434\Desktop\vs_workspaces'


【依赖环境】
  - Python 3.x（需安装 tkinter，通常已内置）
  - VS Code（会自动检测常见安装路径）
  - Windows 系统（VBS 启动器仅支持 Windows）


【故障排查】
  ● 双击 vbs 无反应
    → 检查 Python 是否已安装并添加到 PATH
    → 尝试直接运行：python vs_run.py

  ● 提示"未找到 VSCode"
    → 手动修改 vs_run.py 第 50 行的 vscode_path

  ● 删除访问历史
    → 删除 .workspace_history.json 文件即可


【版本】v1.0
【日期】2025-10-29
