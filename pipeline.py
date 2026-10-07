from pathlib import Path

from faster_whisper import WhisperModel
from faster_whisper.tokenizer import _LANGUAGE_CODES

from bili import download_bilibili_video

BASE_DIR = Path(__file__).resolve().parent

DOWNLOAD_DIR = BASE_DIR / "downloads"
RESULT_DIR = BASE_DIR / "results"
MODEL_DIR = BASE_DIR / "models"

# 常见语言。完整代码以 faster-whisper 的 _LANGUAGE_CODES 为准。
# zh 表示中文。这个模型没有单独的简体开关，汉字输出通常是简体。
COMMON_LANGUAGES = (
    ("zh", "中文"),
    ("en", "英文"),
    ("ja", "日文"),
    ("ko", "韩文"),
    ("yue", "粤语"),
    ("fr", "法文"),
    ("de", "德文"),
    ("es", "西班牙文"),
    ("ru", "俄文"),
    ("auto", "自动识别"),
)


def parse_urls(raw):
    urls = [item.strip() for item in raw.split() if item.strip()]
    if not urls:
        raise ValueError("没有输入任何链接")
    return urls


def resolve_language(language):
    language = language.strip().lower()
    if language == "auto":
        return None
    if language not in _LANGUAGE_CODES:
        common = "，".join(f"{code}={name}" for code, name in COMMON_LANGUAGES)
        accepted = "，".join(_LANGUAGE_CODES)
        raise ValueError(
            f"无法识别的语言代码: {language}。常见选项：{common}。全部代码：{accepted}"
        )
    return language


def ask_urls():
    print("请粘贴链接")
    return parse_urls(input())


def ask_language():
    print("请选择语言")
    for code, name in COMMON_LANGUAGES:
        print(f"  {code}  {name}")
    print("也可以输入 faster-whisper 支持的其他语言代码")
    return resolve_language(input())


def transcribe_video(model, video_path, language):
    print(f"开始转写: {video_path}", flush=True)
    print("正在从视频里解码声音，这一步会占用 CPU，暂时没有进度条。", flush=True)
    segments, info = model.transcribe(
        video_path,
        language=language,
        task="transcribe",
        beam_size=5,
        temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
        condition_on_previous_text=True,
        vad_filter=False,
        log_progress=True,
    )
    print(
        f"声音解码完成，时长 {info.duration:.1f} 秒，识别语言 {info.language}。"
        "下面开始逐段转写。",
        flush=True,
    )
    result_path = RESULT_DIR / f"{Path(video_path).stem}.txt"
    wrote_any = False
    with result_path.open("w", encoding="utf-8", newline="\n") as result_file:
        print(f"转写结果将随时写入: {result_path}", flush=True)
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue
            result_file.write(text + "\n")
            result_file.flush()
            wrote_any = True
            print(f"[{segment.start:.1f}s -> {segment.end:.1f}s] {text}", flush=True)
    if not wrote_any:
        raise RuntimeError(f"转写结果为空: {video_path}")
    print(f"转写完成: {result_path}", flush=True)
    return result_path


def main():
    urls = ask_urls()
    language = ask_language()

    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    video_paths = []
    for url in urls:
        video_paths.extend(download_bilibili_video(url, str(DOWNLOAD_DIR)))

    print(
        "正在下载或加载 whisper small。"
        "权重文件 model.bin 约 484MB，第一次运行会写入 models 目录。",
        flush=True,
    )
    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="float32",
        download_root=str(MODEL_DIR),
    )
    print("模型已就绪。", flush=True)
    for video_path in video_paths:
        transcribe_video(model, video_path, language)


if __name__ == "__main__":
    main()
