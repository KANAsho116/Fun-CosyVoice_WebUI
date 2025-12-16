# Fun-CosyVoice3 日本語 WebUI

Fun-CosyVoice3-0.5B-2512 モデルを使用した日本語対応の音声合成 WebUI です。

## 特徴

- **日本語対応**: 日本語を含む9言語に対応（中国語、英語、日本語、韓国語、ドイツ語、スペイン語、フランス語、イタリア語、ロシア語）
- **ゼロショット音声クローン**: 3秒以上の参照音声から声をクローン
- **制御トークン**: `[breath]`, `[laughter]` などで表現を細かく制御
- **日本語UI**: シンプルで使いやすい日本語インターフェース

## 必要環境

- Python 3.10
- NVIDIA GPU（CUDA対応）
- 8GB以上のVRAM推奨

## インストール

### 1. リポジトリのクローン

```bash
git clone --recursive https://github.com/KANAsho116/Fun-CosyVoice_WebUI.git
cd Fun-CosyVoice_WebUI
git submodule update --init --recursive
```

### 2. Python環境の構築

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### 3. モデルのダウンロード

```bash
python download_model.py
```

または手動でダウンロード:

```python
from huggingface_hub import snapshot_download

snapshot_download('FunAudioLLM/Fun-CosyVoice3-0.5B-2512',
                  local_dir='pretrained_models/Fun-CosyVoice3-0.5B')
```

## 使い方

### WebUIの起動

```bash
python webui_jp.py
```

ブラウザで `http://localhost:7860` にアクセス

### 基本的な使用方法

1. **合成テキスト**: 読み上げたいテキストを入力
2. **参照音声**: クローンしたい声の音声ファイル（3秒以上）をアップロード
3. **参照音声テキスト**: 参照音声で話している内容（任意）
4. **音声生成**: ボタンをクリックして音声を生成

### 制御トークン

テキスト内に以下のトークンを挿入することで、表現を制御できます:

- `[breath]` - 呼吸音
- `[laughter]` - 笑い声
- `[fil]` - フィラー音（えー、あー）

例: `こんにちは。[breath]今日はいい天気ですね。`

## オリジナルリポジトリ

このプロジェクトは [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) をベースにしています。

**Fun-CosyVoice 3.0**: [Demos](https://funaudiollm.github.io/cosyvoice3/) | [Paper](https://arxiv.org/abs/2505.17589) | [HuggingFace](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512)

## ライセンス

このプロジェクトは Apache 2.0 License に基づいています。

## 謝辞

- [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) - オリジナルの CosyVoice 実装
- [Matcha-TTS](https://github.com/shivammehta25/Matcha-TTS)
- [FunASR](https://github.com/modelscope/FunASR)

## 免責事項

このコンテンツは学術目的のみであり、技術的な能力を実証することを目的としています。
