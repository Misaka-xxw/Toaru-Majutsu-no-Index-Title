<center>
<img alt="标题" src="docs/title.png">
<h1 align="center">
某学都的标题工房
</h1>
<h6 align="center">
当科学与魔法交织之时，故事即将开始!
</h6>
<div align="center">
<img alt="Static Badge" src="https://img.shields.io/badge/language-python_3.10-blue" style="margin-right: 5px;">
<img alt="Static Badge" src="https://img.shields.io/github/license/Misaka-xxw/Toaru-Majutsu-no-Index-Title.svg" style="margin-right: 5px;">
<img alt="Static Badge" src="https://img.shields.io/maintenance/yes/2025.svg" style="margin-right: 5px;">

[English](docs/README_en.md) | [日本語](docs/README_jp.md)
</div>
</center>

> 项目正在初步开发中……

## 📖 项目简介
**某学都的标题工房** 是一个用于生成标题设计的工具，灵感来源于《某魔法的禁书目录》和《某科学的超电磁炮》系列。
本项目旨在帮助用户快速生成具有某系列风格的标题，适用于各种场景，如海报设计、视频封面等。

---

## 🚀 功能特性
- **色彩推荐**：提供与原作风格一致的配色方案。
- **高效输出**：快速生成高分辨率的标题图片。

---

## 🔧 安装与使用
### 环境要求
- 推荐使用Python 3.10 或更高版本

### 运行步骤
1. 克隆项目到本地：
   ```bash
   git clone https://github.com/Misaka-xxw/Toaru-Majutsu-no-Index-Title.git
   cd Toaru-Majutsu-no-Index-Title
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行项目：
   ```bash
   python main.py
   ```

---

## 📂 文件结构
```
```

pyinstaller打包成软件（示例）：
```
pyinstaller  --debug all main.py --name TitleGenerator --onefile --windowed --strip --clean --noconfirm --icon icons/favicon.ico --add-data "fonts;fonts" --add-data "icons;icons" --hidden-import=PIL --hidden-import=numpy --exclude-module matplotlib --exclude-module tkinter --exclude-module IPython --exclude-module PyQt6.QtQml --exclude-module PyQt6.QtQuick --exclude-module PyQt6.QtNetwork --exclude-module PyQt6.QtWebEngine --exclude-module PyQt6.QtWebEngineCore --exclude-module PyQt6.QtWebEngineWidgets --exclude-module PyQt6.QtMultimedia --exclude-module PyQt6.QtBluetooth --exclude-module PyQt6.QtPositioning --exclude-module PyQt6.QtSensors --exclude-module PyQt6.QtSql --exclude-module PyQt6.QtTest --exclude-module PyQt6.QtPdf --exclude-module PyQt6.QtPdfWidgets --upx-dir  "D:\software\upx-5.1.1-win64\upx.exe"
```

upx进一步压缩（示例）
```bash
D:\software\upx-5.1.1-win64\upx.exe --best D:\Github\Toaru-Majutsu-no-Index-Title\dist\TitleGenerator.exe --force
```

---

## 🔗 资源与参考
- [字体下载](https://www.fonts.net.cn/font-34110358882.html)
- [平替字体下载](https://m.fontke.com/family/1178214/style/)
- [官方 Wiki](https://toaru.huijiwiki.com)
- [色卡](https://toaru.huijiwiki.com/wiki/%E5%B8%AE%E5%8A%A9:%E9%A2%9C%E8%89%B2)  

---

## 🤝 贡献指南
欢迎任何形式的贡献！  
如果您有任何建议或发现了问题，请提交 [Issue](https://github.com/Misaka-xxw/Toaru-Majutsu-no-Index-Title/issues) 或创建 Pull Request。

---

## 📜 许可证
本项目基于 [GPL-3.0 license](LICENSE) 开源，您可以自由使用、修改和分发。
