#! encoding:UTF-8
import cairosvg
import os

loop = True
while loop:
    svgDir = input("请输入SVG文件目录")
    if os.path.exists(svgDir) and os.path.isdir(svgDir):
        loop = False
    else:
        print
        "错误：您输入的SVG文件目录不存在或者不是一个有效的目录，请重新输入"

loop = True
while loop:
    exportDir = input("请输入导出目录")
    if os.path.exists(exportDir):
        loop = False
    else:
        print
        "错误：您输入的导出目录[", exportDir, "] 不存在，是否要创建这个目录？"
        loops = True
        while loops:
            msg = ""
            cmd = input("创建 (Y) 重新 (R)")
            if cmd.upper() == "R":
                loops = False
            elif cmd.upper() == "Y":
                os.makedirs(exportDir, True)
                if os.path.exists(exportDir):
                    loop = False
                    loops = False
                else:
                    print
                    "创建目录失败[", exportDir, "]， 请重新输入"
            else:
                print
                "找不到您输入的命令，请重新输入"

cate = ("png", "pdf")
print
"导出类型："
for i in cate:
    print
    i

loop = True
while loop:
    exportFormat = input("请输入导出类型")
    if exportFormat.lower() in cate:
        loop = False
    else:
        print("您输入的类型不存在，请重新输入")


def export(fromDir, targetDir, exportType):
    print
    "开始执行转换命令..."
    files = os.listdir(fromDir)
    num = 0
    for fileName in files:
        path = os.path.join(fromDir, fileName)
        if os.path.isfile(path) and fileName[-3:] == "svg":
            num += 1
            fileHandle = open(path)
            svg = fileHandle.read()
            fileHandle.close()
            exportPath = os.path.join(targetDir, fileName[:-3] + exportType)
            exportFileHandle = open(exportPath, 'w')

            if exportType == "png":
                cairosvg.svg2png(bytestring=svg, write_to=exportPath)
            elif exportType == "pdf":
                cairosvg.svg2pdf(bytestring=svg, write_to=exportPath)

            exportFileHandle.close()





export(svgDir, exportDir, exportFormat)

# 该代码片段来自于: http://www.sharejs.com/codes/python/9052