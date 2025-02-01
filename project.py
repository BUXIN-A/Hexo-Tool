import maliang
import yaml
import json5 as json
import os
import tkinter as tk
from librarys import C_json, C_canvas

with open('data\\language\\theme\\{0}'.format(C_json.json_read('data\\config\\data.json', 'language')), 'r', encoding='utf-8') as f:
    HLanguage = json.load(f)

class ProjectWindow(maliang.Toplevel):
    def __init__(self, projectPath):    #需要传入一个项目路径(String)形参：projectPath为项目路径
        super().__init__(size=(1000, 600),
                         position=(500, 200),
                         title="HEXO Tool -Project Window")
        self.projectPath =projectPath
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')
        self.configcanvas = maliang.Canvas(master=self, auto_update=True, width=1000, height=600,
                                     highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.configcanvas.bind('<Configure>', self.on_configure)
        self.configcanvas.bind('<MouseWheel>', self.on_mouse_wheel)
        self.scrollbar.config(command=self.configcanvas.yview)
        self.configcanvas.pack(fill='both', expand=True)
        self.yamlData = self.readYaml()
        self.ui()

        self.configcanvaslist = [self.configcanvas]

    def ui(self):
        for a, i in enumerate(self.yamlData, 0):
            self.Label = maliang.Label(self.configcanvas, position=(10, 10+a*50), size=(350, 40), text=self.VS(i))
            self.InputBox = maliang.InputBox(self.configcanvas, position=(380, 10+a*50), size=(450, 35), placeholder=self.VS(i)).append(str(self.yamlData[i]))
    def on_configure(self, event):
        self.configcanvas.configure(scrollregion=self.configcanvas.bbox('all'))
    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.configcanvas.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.configcanvas.yview_scroll(1, 'units')

    def VS(self, key):
        if key in HLanguage:
            return HLanguage[key]
        else:
            return key

    def QueDingXiuGai(self):
        self.yamlData['title'] = self.title.get()
        self.writeYaml()

    def readYaml(self):
        with open(self.projectPath + "\\_config.yml") as f:
            yamlData = yaml.load(f, Loader=yaml.FullLoader)
        return yamlData

    def writeYaml(self):
        with open(self.projectPath + "\\_config.yml", 'w') as f:
            yaml.safe_dump(self.yamlData, f)

if __name__ == "__main__":
    PW = ProjectWindow("hexo\\versions\\examlp")
    PW.mainloop()