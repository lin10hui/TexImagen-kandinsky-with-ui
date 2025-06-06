# 简介
本项目基于[Kandinsky 2.1](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)模型，使用python语言设计并编写一个独立、具备用户交互功能的图形化程序，旨在实现以下三个功能：  
1.文本生成图像（Text-to-Image, T2I）；  
2.图像修复（Inpainting）；  
3.图像融合（Image Fusion）。  
***本程序有三个版本：远程服务器端、本地端、完整版，请您按需选择**  

## 操作指南  
**第一步：初始化与执行**  
1.使用下列命令在运行环境下载[Kandinsky 2.1](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)模型  
方式一：  
```git clone https://github.com/ai-forever/Kandinsky-2.git  ```   
方式二：  
直接下载本项目中的Kandinsky-2-main文件夹，此文件夹经删减后仅包含Kandinsky 2.1模型。  
2.调用方式有三种：  
注：首次使用必须调用init文件或点击程序“初始化”按钮进行**初始化**。  
a.直接执行不同文件：将文件放入解压好的文件夹内直接运行，init为初始化文件，首次使用需执行，T2I、mixing、rec分别为文本生成图像、图像融合和图像修复三个功能的调用代码，当然，如果你拥有jupyter的话直接运用作者的jupyter notebooks会更方便一些。    
b.python实现ui界面：将文件放入解压好的文件夹外执行，运行index1.py文件【现应为index_xxx.py文件】（目录结构如下图所示）  
![image](https://github.com/user-attachments/assets/49e63e80-ea0d-443c-b00a-419515f2ec2f)    
c.直接双击dist目录下的“.exe”后缀文件  
运行成功后即可正常使用其功能  
**第二步：功能使用**  
在界面底部可选择在本地运行或在远程服务器运行：  
*若选择本地运行可跳过步骤1*  
1.在弹窗输入服务器地址、用户名、密码，点击测试连接按钮，连接成功后点击确认按钮即可连接远程服务器，接下来的文本生成图像、图像融合和图像修复操作都将会在服务器上进行；  
2.点击图像生成、图像融合和图像修复三个按钮会显示不同的页面，输入图像描述并选择图像保存路径后点击生成按钮即可。  
如果在使用过程中遇到问题可点击“帮助”按钮联系我。  

**详细介绍**  
1.	文本生成图像（Text-to-Image, T2I）：  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/1.png)  
2.	图像修复（Inpainting）；  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/2.png)  
3.图像融合（Image Fusion）。  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/3.png)  
	并且本程序包含三个版本：远程服务器端、本地端、完整版，同时满足远程使用与本地使用的需求，并且用户可点击“.exe”后缀文件直接使用。  
远程服务器端：  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/remote.png)  
本地端：  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/host.png)  
完整版：  
 ![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/all.png)  
其余配套功能：  
![image](https://github.com/lin10hui/TexImagen-kandinsky-with-ui/blob/main/img/other.png)  
## 贡献者欢迎  
  
嗨！非常感谢你查看这个项目。作为一个新手小白，我深知自己在编程和项目管理上还有很多需要学习的地方。因此，我非常欢迎和感激任何形式的贡献，无论是修复一个小的bug、优化代码性能、改善文档，还是提出建设性的意见和建议。  
  
你的贡献将对这个项目产生巨大的影响，并帮助我成长为一名更好的开发者。请放心，即使你的改动很小，也会被视为非常宝贵的贡献。  
  
如果你有任何疑问或需要任何帮助，请随时与我联系。我期待着与你一起合作，共同推进这个项目的发展。  
  
## 更新日志
1.上传了4个文件用于初始化和调用Kandinsky 2.1模型，可以在[下载](https://github.com/ai-forever/Kandinsky-2?tab=readme-ov-file)的基础上将文件放入解压好的文件夹内直接运行，init为初始化文件，首次使用需执行，T2I、mixing、rec分别为文本生成图像、图像融合和图像修复三个功能的调用代码，当然，如果你拥有jupyter的话直接运用作者的jupyter notebooks会更方便一些，这些文件的设计仅为后续在ui界面中调用使用。  
2.上传了ui界面的第一个版本，实现了图像生成功能的界面。  
3.上传了完整的ui界面文件index1.py，可以在本地通过运行该文件，实现文本生成图像、图像融合和图像修复三个功能。  
4.上传了可执行文件“TexImagenKandinsky.exe”  
5.更改了完整版无法运行的bug  
6.增加了自定义背景功能  
7.上传了安全性检测报告report.json【使用bandit工具检测】  

