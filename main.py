import threading
from tkinter import messagebox
import maliang
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
import subprocess
import shutil
import json5 as json
import maliang.theme
import time

import librarys.C_json as C_json
import librarys.C_canvas as C_canvas

import project as one

# initialize
theme_list = ['dark', 'light', 'system']
with open('data\\language\\main\\{0}'.format(C_json.json_read('data\\config\\data.json', 'language')), 'r', encoding='utf-8') as f:
    language = json.load(f)
    language_list = os.listdir('data\\language\\main')
    language_name_list = [C_json.json_read('data\\language\\main\\{0}'.format(i), 'language') for i in language_list]
maliang.theme.set_color_mode(C_json.json_read('data\\config\\data.json', 'theme'))
# function
def initialize():
    try:
        node_path = shutil.which('node')
        if node_path:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
            print(f"Node.js 已安装，版本：{result.stdout.strip()}")
            try:
                git_path = shutil.which('git')
                if git_path:
                    result = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
                    print(f"Git 已安装，版本：{result.stdout.strip()}")
                    return True
                else:
                    print("Git 未安装")
                    return False
            except Exception as e:
                print(f"检查 Git 时出错：{e}")
                return False
        else:
            print("Node.js 未安装")
            return False
    except Exception as e:
        print(f"检查 Node.js 时出错：{e}")
        return False
# 退出提示
def exit() -> None:
    if messagebox.askyesno(message=language['root.exit']):
        C_json.json_edit('data\\config\\data.json', 'main_x', str(root.winfo_x()))
        C_json.json_edit('data\\config\\data.json', 'main_y', str(root.winfo_y()))
        root.destroy()
# 获取程序版本
def get_product_version(key):
    try:
        with open('version', 'r', encoding='utf-8') as f:
            version_info = f.read()
            start_marker = f'StringStruct("{key}", "'
            start_index = version_info.find(start_marker)
            if start_index == -1:
                return None
            start_index += len(start_marker)
            end_index = version_info.find('")', start_index)
            if end_index == -1:
                return None
            return version_info[start_index:end_index]
    except Exception as e:
        return f"获取版本号时出错：{e}"
# 切换语言
def LanguageSwitching(i):
    def restart(a):
        if a == 'yes':
            root.destroy()
            subprocess.Popen([sys.executable, __file__])
    if C_json.json_read('data\\config\\data.json', 'language') != language_list[i]:
        C_json.json_edit('data\\config\\data.json', 'language', language_list[i])
        maliang.TkMessage(message=language['root.setting.language.tip'].format(language_name_list[i]), detail=language['root.setting.language.tip2'], option="yesno", command=lambda a:restart(a))
# 切换主题
def ThemeSwitching(i):
    if C_json.json_read('data\\config\\data.json', 'theme') != theme_list[i]:
        C_json.json_edit('data\\config\\data.json', 'theme', theme_list[i])
        maliang.theme.set_color_mode(theme_list[i])
    listbox.config(selectforeground='white')
# 命令行终端
def run_command(command): 
    TKcommand = maliang.Toplevel(root, (800, 550))
    TKcommand.title('HEXOCMD')
    CText = tk.Frame(TKcommand)
    CText.pack(fill='both', expand=True)
    l2 = tk.Label(CText, text='CMD', width=500, justify='left', anchor='w')
    l2.pack()
    s2 = tk.Scrollbar(CText)
    b2 = tk.Scrollbar(CText, orient='horizontal')
    s2.pack(side='right', fill='y')
    b2.pack(side='bottom', fill='x')
    text2 = tk.Text(CText, width=500, height=500, wrap='word', yscrollcommand=s2.set, xscrollcommand=b2.set)
    text2.pack(fill='both', expand=True)
    s2.config(command=text2.yview)
    b2.config(command=text2.xview)
    def run():
        process = subprocess.Popen(
            command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                break
            if output:
                text2.insert('end', output)
        process.wait()
        if process.returncode == 0:
            TKcommand.destroy()
            create.destroy()
            RElistbox(listbox)
        else:
            text2.insert('end', f'error:{process.returncode}')
            time.sleep(3)
            TKcommand.destroy()
            create.destroy()
    threading.Thread(target=run).start()
# 创建项目
def hexo_create_project_Progress(name):
    if name == '':
        maliang.TkMessage(message=language['create.name.empty'])
        return True
    elif os.path.exists('hexo\\versions\\{0}'.format(name)):
        maliang.TkMessage(message=language['create.name.exist'])
        return True
    else:
        time.sleep(5)
        try:
            os.mkdir(os.path.join('hexo\\versions', name))
            path = os.path.abspath(os.path.join('hexo\\versions', name))
            threading.Thread(target=run_command('hexo init {0}'.format(path))).start()
        except Exception as e:
            return f"Error: {e}"

def Wversion_create_project(language):
    global create
    create = maliang.Toplevel(master=root, size=(500, 650), position=(500, 200), title=language['root.version.create'])
    create.resizable(False, False)
    cr = maliang.Canvas(master=create, width=500, height=650, bg='white')
    cr.pack(fill='both', expand=False)
    name = maliang.InputBox(master=cr, position=(10, 10), size=(480, 40), placeholder=language['create.title'])
    maliang.Button(master=cr, position=(10, 600), text=language['create.create'], size=(200, 40), command=lambda:create.destroy() if hexo_create_project_Progress(name.get()) else None)
    maliang.Button(master=cr, position=(290, 600), text=language['create.cancel'], size=(200, 40), command=lambda:create.destroy())

def RElistbox(self):
    self.delete(0, 'end')
    for file in os.listdir('hexo\\versions'):
        self.insert(tk.END, file)

def delete_project():
    if len(listbox.curselection()) == 0:
        maliang.TkMessage(message=language['root.version.delete.empty'])
    else:
        selected = listbox.get(listbox.curselection())
        try:
            if messagebox.askyesno(message=language['root.version.delete.tip']):
                shutil.rmtree(os.path.join('hexo\\versions', selected))
                RElistbox(listbox)
        except Exception as e:
            maliang.TkMessage(message=e)

def open_project():
    if len(listbox.curselection()) == 0:
        maliang.TkMessage(message=language['root.version.open.empty'])
    else:
        selected = listbox.get(listbox.curselection())
        try:
            one.ProjectWindow(os.path.join('hexo\\versions', selected))
        except Exception as e:
            maliang.TkMessage(message=e)

#tkinter&maliang
root = maliang.Tk((1200, 800), (int(C_json.json_read('data\\config\\data.json', 'main_x')), int(C_json.json_read('data\\config\\data.json', 'main_y'))), title="HEXO Tool")
root.at_exit(exit, ensure_destroy=False)
root.icon('img/hexo.ico')
root.resizable(False, False)
rootcv = maliang.Canvas(master=root, auto_update=True, width=100, highlightthickness=0)
rootcv.pack(side='left', fill='y', expand=False)
# 主页 ------
home = maliang.Canvas(master=root, auto_update=True, width=1100, height=800, highlightthickness=0)
home.pack(side='left', expand=True)
maliang.Text(master=home, text=language['root.home.welcome'], position=(550, 30), fontsize=30, weight='bold', anchor='center')
maliang.Text(master=home, text=get_product_version('ProductVersion'), position=(0, 0), fontsize=10, weight='bold')
maliang.Button(master=home, text=language['root.home.sponsor'], position=(550, 100), command=lambda:subprocess.Popen(['start', 'https://buxin.us.kg/'], shell=True))
# 项目界面 ------
version = maliang.Canvas(master=root, auto_update=True, width=1100, height=800, highlightthickness=0)
version.pack(side='left', expand=True)
maliang.Button(master=version, position=(10, 10), text=language['root.version.create'], size=(140, 40), command=lambda:Wversion_create_project(language))
maliang.Button(master=version, position=(10, 60), text=language['root.version.delete'], size=(140, 40), command=lambda:delete_project())
maliang.Button(master=version, position=(10, 110), text=language['root.version.open'], size=(140, 40), command=lambda:open_project())
maliang.Button(master=version, position=(10, 160), text=language['root.version.refresh'], size=(140, 40), command=lambda:RElistbox(listbox))
scrollbar = tk.Scrollbar(version)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(version, width=960, height=750, selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
RElistbox(listbox)
listbox.pack(padx=160, pady=0, fill='x')
# 设置页面 ------
settings = maliang.Canvas(master=root, auto_update=True, width=1100, height=800, highlightthickness=0)
settings.pack(side='left', expand=True)
# language
maliang.Text(master=settings, text=language['root.setting.language'], position=(10, 10), fontsize=20)
maliang.OptionButton(master=settings, position=(120, 5), text=(language_name_list), default=language_list.index(C_json.json_read('data\\config\\data.json', 'language')), command=lambda i:LanguageSwitching(i))
# theme
maliang.Text(master=settings, text=language['root.setting.theme'], position=(10, 60), fontsize=20)
maliang.OptionButton(master=settings, position=(120, 55), text=(language['root.setting.theme.dark'], language['root.setting.theme.light'], language['root.setting.theme.system']), default=theme_list.index(C_json.json_read('data\\config\\data.json', 'theme')), command=lambda i:ThemeSwitching(i))

canvases = [home, version, settings]

maliang.SegmentedButton(master=rootcv, position=(0, 0), text=(language['root.home'], language["root.version"], language["root.setting"]), layout="vertical", fontsize=18, weight='bold', default=0, command=lambda i:C_canvas.Toggle_Canvas(rootcv.getint(i), canvases), sizes=[(85, 40), (85, 40), (85, 40)])
C_canvas.Toggle_Canvas(rootcv.getint(0), canvases)

if initialize():
    try:
        if shutil.which('hexo'):
            print("Hexo 已安装")
    except Exception as e:
        try:
            print("Hexo 未安装，正在安装...")
            subprocess.run(['npm', 'install', 'hexo'], check=True)
            print("Hexo 安装完成")
        except Exception as e:
            print(f"安装 Hexo 时出错：{e}")
            root.destroy()
    root.mainloop()
else:
    maliang.TkMessage(message='Tip', detail=language['root.initialize.one'], title='error', option='ok', icon='warning')
    root.destroy()