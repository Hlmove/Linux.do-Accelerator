# linuxdo-accelerator

一个原生 Rust 的 `linux.do` 专属加速器，同时提供：

- 单一二进制：同一个 `linuxdo-accelerator` 同时支持 `CLI` 和桌面 `GUI`
- `CLI`：适合脚本和终端操作
- 桌面壳：双击启动 GUI，点击“加速/停止”，支持最小化
- 一键生成并安装本地根证书
- 一键写入 `hosts`
- 本地监听 `80/443`
- 将 `linux.do` / `www.linux.do` 反向代理回真实站点

适合直接作为 GitHub 首页说明的摘要：

- 原生 Rust 开发，不依赖 Node 运行时
- Windows / Linux / macOS 三端统一交付
- 单程序同时支持双击启动和命令行调用
- 配置集中在一个 `linuxdo-accelerator.toml` 文件
- 支持一键安装证书、接管域名、DoH 和本地监听

## 二进制结构

- `linuxdo-accelerator`
  - 单一二进制，同时支持 CLI 和原生桌面 GUI
  - 无参数时打开 GUI
  - 传入子命令时按 CLI 模式运行
  - Windows 双击打开弹窗
  - Linux 安装后可从桌面入口打开
  - macOS 可打包为 `.dmg`

## GUI 行为

- 双击打开桌面窗口
- 点击“加速”时，如果当前没有管理员权限，会触发系统提权确认
- 启动后按钮会切换成“停止”
- 加速启动后可直接点击“最小化”
- GUI 本身不承载代理逻辑，真正的监听服务会由后台守护进程运行

## CLI 使用

初始化配置：

```bash
cargo run --bin linuxdo-accelerator -- init-config
```

准备证书和 hosts：

```bash
sudo cargo run --bin linuxdo-accelerator -- setup
```

前台直接启动：

```bash
sudo cargo run --bin linuxdo-accelerator -- start
```

停止后台加速：

```bash
sudo cargo run --bin linuxdo-accelerator -- stop
```

查看状态：

```bash
cargo run --bin linuxdo-accelerator -- status
```

## GUI 开发运行

```bash
cargo run --bin linuxdo-accelerator
```

## 打包

项目提供了 `cargo-packager` 配置文件 [Packager.toml](/home/catcatyu/桌面/linuxdo/Packager.toml)：

- Windows 目标格式：`NSIS .exe`
- Linux 目标格式：`.deb`
- macOS 目标格式：`.dmg`

本地手动打包：

```bash
cargo install cargo-packager --locked
cargo packager --release -c Packager.toml
```

只打 Linux `deb`：

```bash
cargo packager -f deb --release -c Packager.toml
```

当前本机已经验证可以产出：

```text
dist/linuxdo-accelerator_0.1.0_amd64.deb
```

macOS 不再走本地交叉编译脚本，改为使用 GitHub Actions 工作流 [.github/workflows/build-release.yml](/home/catcatyu/桌面/linuxdo/.github/workflows/build-release.yml) 在 `macos-latest` runner 上原生构建 `.dmg`。

工作流会分别在三端原生 runner 上打包：

- Linux：生成 `.deb`
- Windows：生成 `NSIS .exe`
- macOS：生成 `.dmg`

## 配置文件

默认情况下，程序只使用一个主配置文件 `linuxdo-accelerator.toml`。三端默认位置如下：

- Linux
  - 配置文件：`~/.config/linuxdo-accelerator/linuxdo-accelerator.toml`
  - 运行状态目录：`~/.local/share/linuxdo-accelerator/runtime`
  - 证书目录：`~/.local/share/linuxdo-accelerator/certs`
- Windows
  - 配置文件：`%APPDATA%\linuxdo\linuxdo-accelerator\config\linuxdo-accelerator.toml`
  - 运行状态目录：`%LOCALAPPDATA%\linuxdo\linuxdo-accelerator\data\runtime`
  - 证书目录：`%LOCALAPPDATA%\linuxdo\linuxdo-accelerator\data\certs`
- macOS
  - 配置文件：`~/Library/Application Support/io.linuxdo.linuxdo-accelerator/linuxdo-accelerator.toml`
  - 运行状态目录：`~/Library/Application Support/io.linuxdo.linuxdo-accelerator/runtime`
  - 证书目录：`~/Library/Application Support/io.linuxdo.linuxdo-accelerator/certs`

如果你启动时显式传了 `--config /path/to/linuxdo-accelerator.toml`，程序会改用你指定的那一份配置文件；对应的 `runtime` 和 `certs` 目录也会优先跟着这个配置目录走。

配置文件内容类似：

```toml
listen_host = "127.0.0.1"
hosts_ip = "127.0.0.1"
http_port = 80
https_port = 443
upstream = "https://linux.do"
proxy_domains = ["linux.do", "www.linux.do"]
certificate_domains = ["linux.do", "www.linux.do", "*.linux.do"]
ca_common_name = "Linux.do Accelerator Root CA"
server_common_name = "linux.do"
```

## 当前边界

- 当前仍是站点专属反向代理，不是系统全局代理
- 当前只实现 `HTTP/HTTPS`
- WebSocket 透传还未单独补齐

## 参考项目

- `dev-sidecar`: https://github.com/docmirror/dev-sidecar
- `steamcommunity302`: 交互形态和本地接管思路参考
