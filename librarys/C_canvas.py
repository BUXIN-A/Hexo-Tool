import maliang
def Toggle_Canvas(num: int, canvases: list[maliang.Canvas]) -> None:
    for canvas in canvases:
        canvas.pack_forget()
    canvases[num].pack()
    canvases[num].update()
    canvases[num].zoom()