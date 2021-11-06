<!--
 * @Description: Rolin's code edit
 * @Author: Rolin-Code
 * @Date: 2021-11-05 00:13:18
 * @LastEditors: Rolin
 * @Code-Function-What do you want to do: 
-->
## Gdipcna
# GDIP Campus Network Assistant

<p align="center">
  <h1 align="center" style="margin: 0 auto 0 auto;">广轻校园网助手</h1>
  <h5 align="center" style="margin: 0 auto 0 auto;">GDIP Campus Network Assistant</h5>
  </p>

  <p align="center">
    <img src="https://img.shields.io/github/last-commit/8808-Rolin/GDIP-network-assistant">
    <img src="https://img.shields.io/github/contributors/8808-Rolin/GDIP-network-assistant">
    <img src="https://img.shields.io/github/issues/8808-Rolin/GDIP-network-assistant?label=issues">
    <img src="https://img.shields.io/github/stars/8808-Rolin/GDIP-network-assistant">
  </p>

  <br>

- [GDIP Campus Network Assistant](#gdip-campus-network-assistant)
- [Developers Information](#developers-information)
- [Update-History](#update-history)
  - [Version 1.0](#version-10)
  - [Version 2.0](#version-20)
  - [Version 3.0](#version-30)
  - [Version 4.0](#version-40)
- [Usage](#usage)
  - [具体使用方法](#具体使用方法)
  - [加入开机自启动](#加入开机自启动)
- [Code-Usage](#code-usage)

# Developers Information
[Developer's Bilibili](https://space.bilibili.com/23161464)

Proposer:
- 星淡
- 30202的大家
# Update-History
## Version 1.0
- Ver 1.0 初版软件推出
- Ver 1.1 新增 Linux版本
- Ver 1.2 新增 账号密码，增强适配性
- Ver 1.3 新增 配置文件管理，更加方便的使用校园网
## Version 2.0
- Ver 2.0 新增 图形界面GUI ，使得操作更加便捷与人性化,开机即连 无人值守，Linux版本和桌面版本分开开发
- Ver 2.0.1 修复 移动状态下IP仍旧不变的问题(路由模式->直连模式)
- Ver 2.1 优化 用户体验；优化 直连模式和路由模式兼容 路由模式和直连不再做模式区分；修复 一些已知的BUG
- Ver 2.2 新增 一键连接，摆脱开机等十秒；优化 控制台信息输出内容，密码不再输出
- Ver 2.3 修复 登录失败显示乱码的问题；优化 重连机制；新增 保存到日志功能；
- Ver 2.5 优化 脚本正式更名‘广轻网络助手’;新增 建议/反馈功能，随时吐槽;新增 更新模块
- ver 2.5.2 修复 一些已知的BUG;新增 状态栏随着网络状况的变化而变化
- ver 2.5.6 修复 一些可能导致崩溃的bug;优化 用户体验;更改 进入正式版内测阶段;新增 采用自压缩包安装方式
- ver 2.5.7 优化 每次打开软件时都将检测新版本更新
- ver 2.5.8 优化 修复一些BUG
- ver 2.5.9 优化 自动更新的bug 添加了更多的线程
## Version 3.0
- Ver 3.0 修复断网异常，增加更多鲁棒性，采用单文件形式，不再解压安装
- Ver 3.2 修复更多异常 提高使用稳定性
- Ver 3.4 提高稳定性，修复异常，在网络波动时更加智能
- Ver 3.7 财力不足，放弃了自动更新模块（实在没钱续费啦）
- Ver 3.8 提高稳定性，修复更多异常，就是机房暂时炸了也不影响软件正常使用
## Version 4.0 
- Ver 4.0 船新改版上线
  - 新增 集成路由模式，跨路由也可以使用该助手维持在线状态
  - 新增 用户IP实时上传云端，随时可以通过Web查找当前IP
  - 优化 重构界面UI，二刺螈气息UP UP UP，阿门
  - 优化 重构代码结构，优化逻辑处理 提高程序运行效率
  - 优化 日志系统，现在日志有时间了，能够更加快速的定位BUG
  - 优化 在联网第一次使用该脚本时，能够智能的获取当前学号
  - 修复 在校园网内使用因为DNS劫持而无法正常工作的BUG
  - 修复 在机房爆炸的时候会自动结束进程的BUG
- Ver 4.1 最强日志版本
  - 新增 实装V2日志引擎，找BUG不用愁
  - 修复 一些些联网BUG
  - 修复 界面UI不协调


# Usage
- 使用场景：广东轻工职业技术学院校园网
- 能且仅能在校园网环境下正常工作
## 具体使用方法
- 第一次使用时需要设置校园网账号密码，随后该账号密码会被记录，以后再打开软件将会自动读取配置文件进行登录
- 请务必确保账号密码的正确性
- 该软件完成了掉线自动登录功能，7x24小时无人值守
- 加入自启动后能实现开机即连功能，开机即连
## 加入开机自启动
1. Win+R 打开运行窗口
2. 输入 `shell:startup` 打开启动项文件资源管理器
3. 将本软件的**快捷方式**复制到文件夹下即可
# Code-Usage
- pyinstaller编译教程：
编译命令：pyinstaller -F -w -i ./assets/favicon.ico main.py -p wind.py -p utils.py -p network.py -p config.py --add-data ".\\assets\\*;.\\assets"
