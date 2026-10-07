# Bili-Video2Text

把一个或多个哔哩哔哩视频链接下载到本地，再用 whisper `small` 在 CPU 上转写成文字。

- Python：3.12
- 包管理：`uv`（不要用 conda）
- 转写：`faster-whisper`，设备固定 CPU，计算精度 `float32`
- 模型：第一次运行会从 Hugging Face 拉取 `Systran/faster-whisper-small`，权重 `model.bin` 约 484MB，保存在本仓库的 `models` 目录
- 系统依赖：需要能在命令行直接运行 `ffmpeg`，`yt-dlp` 合并视频和音频时会用到


## Windows

在 PowerShell 中安装 `uv`：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

也可以用 WinGet：

```powershell
winget install --id=astral-sh.uv -e
```

安装 `ffmpeg`，并确认命令可用：

```powershell
winget install ffmpeg
ffmpeg -version
```

关闭并重新打开 PowerShell，进入仓库目录后创建虚拟环境并安装依赖：

```powershell
cd 你的路径\Bili-Vid2Text
uv venv --python 3.12 .venv
.\.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

如果执行激活脚本被拦截，后面的 `python` 改成：

```powershell
.\.venv\Scripts\python.exe
```

运行：

```powershell
python pipeline.py
```

## macOS

安装 `uv`：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

也可以用 Homebrew：

```bash
brew install uv
```

安装 `ffmpeg`：

```bash
brew install ffmpeg
ffmpeg -version
```

进入仓库目录，创建虚拟环境并安装依赖：

```bash
cd 你的路径/Bili-Vid2Text
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

运行：

```bash
python pipeline.py
```

## Linux

安装 `uv`：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

若没有 `curl`：

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

安装 `ffmpeg`（按发行版选一条）：

```bash
# Debian / Ubuntu
sudo apt update && sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```

确认：

```bash
ffmpeg -version
```

进入仓库目录，创建虚拟环境并安装依赖：

```bash
cd 你的路径/Bili-Vid2Text
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

运行：

```bash
python pipeline.py
```

## 使用方式

1. 执行 `python pipeline.py`
2. 出现「请粘贴链接」后，粘贴一个或多个哔哩哔哩网址，多个网址写在同一行、中间用空格分开，然后回车
3. 出现「请选择语言」后，输入语言代码并回车

常见语言代码：

| 代码 | 含义 |
| --- | --- |
| `zh` | 中文（默认就选这个） |
| `en` | 英文 |
| `ja` | 日文 |
| `ko` | 韩文 |
| `yue` | 粤语 |
| `fr` | 法文 |
| `de` | 德文 |
| `es` | 西班牙文 |
| `ru` | 俄文 |
| `auto` | 根据音频开头自动识别 |

也可以输入 faster-whisper 支持的其他语言代码。

程序会先按顺序下载全部视频，模型只加载一次，再按同样顺序逐个转写。转写时每一段文字会立刻写入对应的结果文件。

## 目录

| 路径 | 内容 |
| --- | --- |
| `downloads/` | 下载好的视频 |
| `results/` | 转写文字，文件名与视频标题相同，扩展名 `.txt` |
| `models/` | whisper `small` 权重；第一次运行自动下载 |
| `.venv/` | 本仓库的 Python 虚拟环境 |

