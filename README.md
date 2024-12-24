# TexImagen-kandinsky-with-ui
具有文本到图像（Text-to-Image, T2I）、修复（Restoration）和图像融合（Image Fusion）三大功能的图形化程序

# 简介
本项目基于[Kandinsky 2.1](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)模型，使用python语言设计并编写一个独立、具备用户交互功能的图形化程序，旨在实现以下三个功能：  
1.文本生成图像（Text-to-Image, T2I）；  
2.图像修复（Inpainting）；  
3.图像融合（Image Fusion）。  

## 操作指南  
**第一步：初始化与执行**  
1.使用下列命令在运行环境下载[Kandinsky 2.1](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)模型  
```git clone https://github.com/ai-forever/Kandinsky-2.git  ```  
2.调用方式有两种：  
a。直接执行不同文件：将文件放入解压好的文件夹内直接运行，init为初始化文件，首次使用需执行，T2I、mixing、rec分别为文本生成图像、图像融合和图像修复三个功能的调用代码，当然，如果你拥有jupyter的话直接运用作者的jupyter notebooks会更方便一些。
b.python实现ui界面：将文件放入解压好的文件夹外执行，运行index1.py文件（目录结构如下图所示）  
![image](https://github.com/user-attachments/assets/49e63e80-ea0d-443c-b00a-419515f2ec2f)  
运行成功后即可正常使用其功能，第一次运行的需要额外进行初始化操作：在界面左上方点击初始化按钮即可。  
**第二步：功能使用**  

  

## 贡献者欢迎  
  
嗨！非常感谢你查看这个项目。作为一个新手小白，我深知自己在编程和项目管理上还有很多需要学习的地方。因此，我非常欢迎和感激任何形式的贡献，无论是修复一个小的bug、优化代码性能、改善文档，还是提出建设性的意见和建议。  
  
你的贡献将对这个项目产生巨大的影响，并帮助我成长为一名更好的开发者。请放心，即使你的改动很小，也会被视为非常宝贵的贡献。  
  
如果你有任何疑问或需要任何帮助，请随时与我联系。我期待着与你一起合作，共同推进这个项目的发展。  
  
## 更新日志
1.上传了4个文件用于初始化和调用Kandinsky 2.1模型，可以在[下载](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)的基础上将文件放入解压好的文件夹内直接运行，init为初始化文件，首次使用需执行，T2I、mixing、rec分别为文本生成图像、图像融合和图像修复三个功能的调用代码，当然，如果你拥有jupyter的话直接运用作者的jupyter notebooks会更方便一些，这些文件的设计仅为后续在ui界面中调用使用。  
2.上传了ui界面的第一个版本，实现了图像生成功能的界面。  
3.上传了完整的ui界面文件index1.py，可以在本地通过运行该文件，实现文本生成图像、图像融合和图像修复三个功能。  
