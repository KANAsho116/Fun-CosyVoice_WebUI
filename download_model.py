#!/usr/bin/env python3
"""
Fun-CosyVoice3 モデルダウンロードスクリプト
HuggingFace Hub からモデルをダウンロードします
"""

import os
import sys

def main():
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("huggingface_hub がインストールされていません")
        print("pip install huggingface_hub でインストールしてください")
        sys.exit(1)

    # モデル保存先ディレクトリ
    models_dir = os.path.join(os.path.dirname(__file__), "pretrained_models")
    os.makedirs(models_dir, exist_ok=True)

    print("=" * 60)
    print("Fun-CosyVoice3 モデルダウンロード")
    print("=" * 60)

    # Fun-CosyVoice3-0.5B モデル
    print("\n[1/2] Fun-CosyVoice3-0.5B-2512 をダウンロード中...")
    print("※ 約4GB程度のダウンロードが必要です")
    try:
        snapshot_download(
            "FunAudioLLM/Fun-CosyVoice3-0.5B-2512",
            local_dir=os.path.join(models_dir, "Fun-CosyVoice3-0.5B"),
            resume_download=True
        )
        print("[OK] Fun-CosyVoice3-0.5B-2512 のダウンロード完了")
    except Exception as e:
        print(f"[ERROR] ダウンロードに失敗しました: {e}")
        sys.exit(1)

    # CosyVoice-ttsfrd（テキスト正規化、オプション）
    print("\n[2/2] CosyVoice-ttsfrd をダウンロード中（オプション）...")
    try:
        snapshot_download(
            "FunAudioLLM/CosyVoice-ttsfrd",
            local_dir=os.path.join(models_dir, "CosyVoice-ttsfrd"),
            resume_download=True
        )
        print("[OK] CosyVoice-ttsfrd のダウンロード完了")
    except Exception as e:
        print(f"[WARN] ttsfrd のダウンロードに失敗しました（オプションなので続行可能）: {e}")

    print("\n" + "=" * 60)
    print("ダウンロード完了！")
    print("WebUIを起動するには: python webui_jp.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
