# PanHub
聚合网盘搜索,配置多个来源搜索夸克网盘资源
短剧资源: https://xn--b9wp0p59gf4o.com/

![Snipaste_2024-12-02](https://yymhtc.oss-cn-beijing.aliyuncs.com/image/Snipaste_2024-12-02.png)

##  功能

- **多来源搜索：** 在多个配置的来源中搜索资源。
- **可定制搜索：** 启用或禁用特定来源，并设置每页显示的结果数量。
- **高级搜索选项：** 按日期、文件类型和文件大小过滤结果。
- **搜索历史：** 查看和管理之前的搜索查询。
- **响应式设计：** 提供用户友好的界面和自定义样式。

## win整合包



夸克链接：https://pan.quark.cn/s/59b84d4aa3d5

百度链接:  https://pan.baidu.com/s/1iB8bHZk7Ya5KgrnAERygQw?pwd=YYMH 

下载解压后双击start.bat启动



## 手动安装

### 前提条件

- 需安装[Miniconda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe)

  

### 步骤

1. **克隆仓库**

   ```
   git clone https://github.com/yourusername/quark-netdisk-search.git
   cd PanHub
   ```

2. **安装conda虚拟环境/依赖**

   ```
   conda_setup.bat
   ```

3. **运行应用程序**

   启动 Streamlit 应用程序：

   ```
   start.bat
   ```

   应用程序将在默认的网络浏览器中打开。

## 配置

该应用程序使用配置文件 (`config.py`) 来管理搜索来源、用户代理和自定义样式。您可以修改此文件以调整应用程序的行为：

- **SEARCH_SOURCES：** 配置每个搜索来源的名称、URL 和优先级。
- **USER_AGENTS：** 指定用于 HTTP 请求的用户代理列表。
- **CUSTOM_CSS：** 自定义应用程序的样式。

## 使用说明

1. 在搜索框中输入关键词并点击“搜索”按钮。
2. 通过侧边栏启用或禁用搜索来源，并选择每页显示的结果数量。
3. 使用高级搜索选项进一步过滤搜索结果。
4. 查看搜索历史以快速访问之前的查询。

## 贡献

欢迎对本项目进行贡献！请通过提交问题或拉取请求与我们联系。

## 许可证

该项目基于 Apache 许可证开源。有关详细信息，请参阅 LICENSE 文件。
