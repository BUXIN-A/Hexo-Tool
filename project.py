import maliang
import yaml
import json5 as json
import os
from librarys import C_json, C_canvas

with open('data\\language\\theme\\{0}'.format(C_json.json_read('data\\config\\data.json', 'language')), 'r', encoding='utf-8') as f:
    language = json.load(f)
    print(language)


class ProjectWindow(maliang.Tk):
    def __init__(self, projectPath):    #需要传入一个项目路径(String)形参：projectPath为项目路径
        super().__init__(size=(1000, 600),
                         position=(500, 200),
                         title="HEXO Tool -Project Window")
        self.projectPath =projectPath
        self.canvas = maliang.Canvas(master=self, auto_update=True, width=1000, height=600,
                                     highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.yamlData = self.readYaml()

        self.canvaslist = [self.canvas]
        self.ui()

    def ui(self):
        self.title = maliang.InputBox(self.canvas, (20, 20), placeholder=self.yamlData['title'])
        self.qdan = maliang.Button(self.canvas, (20, 60), text="确定修改", command=self.QueDingXiuGai)

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