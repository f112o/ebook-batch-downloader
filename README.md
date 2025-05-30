# 电子书自动下载工具
> **⚠️ 注意：不要大批量下载！Don't download for a large quantity!**

本项目基于 Flask + requests + BeautifulSoup 实现，可以通过网页输入书名和数量，自动获取 1lib.sk 上的 PDF 电子书下载链接，并在浏览器端直接下载。

## 功能简介

- 支持输入关键词和数量，自动爬取 1lib.sk 搜索结果
- 只下载 PDF 格式的电子书
- 前端页面美观，操作简单
- 支持多本书批量下载

## 前端界面预览

![前端界面截图](image.png)

## 使用方法

### 1. 安装依赖

```bash
pip install flask requests beautifulsoup4
```

### 2. 配置 Cookie

请将你在 1lib.sk 网站登录后的 Cookie 填写到 `app.py` 和 `get_books.py` 的 headers 变量中，否则可能无法正常下载。

### 3. 启动服务

直接启用下载脚本：
```bash
bash run_download.sh
```
启动网页服务：
```bash
python app.py
```

### 4. 打开网页

浏览器访问 [http://localhost:5000](http://localhost:5000)，输入书名和数量，点击“获取并下载”即可。

## 目录结构

```
├── app.py              # Flask 后端主程序
├── get_books.py        # 电子书爬取与下载逻辑
├── pars.py             # 命令行批量下载脚本（支持参数）
├── run_download.sh     # Bash 批量下载示例脚本
├── templates/
│   └── index.html      # 前端页面
├── image.png           # 前端界面截图
├── README.md           # 项目说明
```

## 注意事项

- 本工具仅供学习和交流使用，请勿用于任何商业或非法用途。
- 1lib.sk 可能会变更页面结构或反爬策略，如遇失效请自行调整代码。
- 下载速度受限于目标网站，请勿频繁请求以免被封禁。

## 常见问题

- **下载的不是 PDF 文件？**  
  请检查 Cookie 是否正确，或目标书籍是否有 PDF 格式。

- **下载失败或提示无链接？**  
  可能是关键词无结果，或目标网站反爬，建议更换 Cookie 或降低请求频率。

---

如有问题欢迎反馈！