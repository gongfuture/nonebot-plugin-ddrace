<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://ddnet.org/ddnet.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ddrace

_✨ 提供 DDNet 成绩查询功能 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/gongfuture/nonebot-plugin-ddrace.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ddrace">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ddrace.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>


## 📖 介绍

这是一个 nonebot2 插件，提供 DDNet 成绩查询功能
可以查询玩家的成绩~~，服务器的状态等信息(还没写好)~~，使用图片发送(这个真有)

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ddrace

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ddrace
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-ddrace
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-ddrace
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-ddrace
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ddrace"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项  | 必填  | 类型 | 默认值 |   说明   |
| :-----: | :---: | :---: |  :----: | :------: |
| ddr_need_at |  否   | Bool|   False   | 是否需要at bot触发指令 |

## 🎉 使用
### 指令表
| 指令  | 权限  | 需要@ | 范围  |   说明   |
| :---: | :---: | :---: | :---: | :------: |
| points | 群员  |  跟随全局   | 群聊，私聊  | 指令说明 |
### 效果图
如果有效果图的话
