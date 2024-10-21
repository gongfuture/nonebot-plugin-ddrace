<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://ddnet.org/ddnet.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ddrace

_✨ 提供 DDNet 成绩查询功能 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/gongfuture/nonebot-plugin-ddrace.svg?style=for-the-badge" alt="license">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge" alt="python">
<a href="https://pypi.python.org/pypi/nonebot-plugin-ddrace">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ddrace.svg?style=for-the-badge" alt="pypi">
</a>
<a href="https://www.codefactor.io/repository/github/gongfuture/nonebot-plugin-ddrace">
<img src="https://img.shields.io/codefactor/grade/github/gongfuture/nonebot-plugin-ddrace?style=for-the-badge">
</a>
<a href="https://github.com/gongfuture/nonebot-plugin-ddrace/commits/main">
<img src="https://img.shields.io/github/last-commit/gongfuture/nonebot-plugin-ddrace?style=for-the-badge">
</a>
<a href="https://wakatime.com/@gongfuture"><img src="https://wakatime.com/badge/github/gongfuture/nonebot-plugin-ddrace.svg?style=for-the-badge" /></a>
<a href="https://qm.qq.com/q/OfK3d9r6o2"><img src="https://img.shields.io/badge/QQ群-611124274-blue?logo=tencentqq&style=for-the-badge" /></a>


</div>


## 📖 介绍

这是一个 nonebot2 插件，提供 DDNet 成绩查询功能
可以查询玩家的成绩， ~~服务器的状态等信息(还没写好)，~~ 使用图片发送(这个真有)

Python新手项目，代码质量低，欢迎各位大佬指导/PR

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
| ddr_at_back |  否   | Bool|   False   | 是否at回发送指令者 |
| ddr_reply |  否   | Bool|   False   | 是否引用指令消息 |
| ddr_priority |  否   | Int |   10       | 优先级，越小越优先，最低为1 |
<!-- | ddr_command_pre_alias |  否   | Str |   ""       | 指令前缀别名，用于和其他插件指令防撞 | -->
| ddr_cache_time |  否   | Int |   60     | 缓存时间，单位为分钟，为 0 时不缓存 |

## 🎉 使用
### 指令表
| 指令  | 权限  | 需要@ | 范围  |   说明   |
| :---: | :---: | :---: | :---: | :------: |
| points | 群员  |  跟随全局   | 群聊，私聊  | 查询{name}的成绩图 |
| fpoints| 群员  |  跟随全局   | 群聊，私聊  | 查询{name}的成绩图(不使用缓存) |
### 效果图
如果有效果图的话
