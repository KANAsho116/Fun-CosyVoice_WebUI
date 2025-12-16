#!/usr/bin/env python3
"""
Fun-CosyVoice3 日本語 WebUI
Gradio を使用した日本語対応の音声合成インターフェース
"""

import os
import sys
import tempfile
import argparse

# Matcha-TTS のパスを追加
sys.path.append(os.path.join(os.path.dirname(__file__), "third_party", "Matcha-TTS"))

import gradio as gr
import torch
import torchaudio


def load_model(model_dir: str):
    """モデルを読み込む"""
    from cosyvoice.cli.cosyvoice import AutoModel

    print(f"モデルを読み込み中: {model_dir}")
    cosyvoice = AutoModel(model_dir=model_dir)
    print("モデルの読み込み完了")
    return cosyvoice


def generate_speech(
    text: str,
    prompt_audio: str,
    prompt_text: str,
    stream: bool,
    cosyvoice
) -> str:
    """
    音声を生成する

    Args:
        text: 合成するテキスト
        prompt_audio: 参照音声ファイルのパス
        prompt_text: 参照音声のテキスト（オプション）
        stream: ストリーミング出力を使用するか
        cosyvoice: モデルインスタンス

    Returns:
        生成された音声ファイルのパス
    """
    if not text:
        raise gr.Error("合成テキストを入力してください")

    if not prompt_audio:
        raise gr.Error("参照音声をアップロードしてください")

    # プロンプトテキストの構築
    # Fun-CosyVoice3 では "You are a helpful assistant.<|endofprompt|>" プレフィックスが必要
    if prompt_text:
        full_prompt = f"You are a helpful assistant.<|endofprompt|>{prompt_text}"
    else:
        full_prompt = "You are a helpful assistant.<|endofprompt|>"

    # 音声生成
    try:
        audio_chunks = []
        for output in cosyvoice.inference_zero_shot(
            text,
            full_prompt,
            prompt_audio,
            stream=stream
        ):
            audio_chunks.append(output["tts_speech"])

        # 音声チャンクを結合
        if audio_chunks:
            audio = torch.cat(audio_chunks, dim=1)

            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                output_path = f.name

            torchaudio.save(output_path, audio, cosyvoice.sample_rate)
            return output_path
        else:
            raise gr.Error("音声の生成に失敗しました")

    except Exception as e:
        raise gr.Error(f"音声生成エラー: {str(e)}")


def create_ui(cosyvoice):
    """Gradio UI を作成"""

    with gr.Blocks(
        title="Fun-CosyVoice3 日本語音声合成",
        theme=gr.themes.Soft()
    ) as demo:
        gr.Markdown(
            """
            # Fun-CosyVoice3 日本語音声合成

            テキストを入力し、参照音声をアップロードして音声を生成します。

            **使い方:**
            1. 合成したいテキストを入力
            2. クローンしたい声の音声ファイル（3秒以上推奨）をアップロード
            3. 必要に応じて参照音声のテキストを入力
            4. 「音声生成」ボタンをクリック

            **制御トークン:** `[breath]`（呼吸音）, `[laughter]`（笑い声）, `[fil]`（フィラー音）
            """
        )

        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="合成テキスト",
                    placeholder="読み上げたいテキストを入力してください...",
                    lines=5
                )

                with gr.Row():
                    prompt_audio = gr.Audio(
                        label="参照音声（3秒以上推奨）",
                        type="filepath",
                        sources=["upload", "microphone"]
                    )
                    prompt_text = gr.Textbox(
                        label="参照音声のテキスト（任意）",
                        placeholder="参照音声で話している内容を入力（省略可）...",
                        lines=3
                    )

                with gr.Row():
                    stream_checkbox = gr.Checkbox(
                        label="ストリーミング出力",
                        value=False,
                        info="チャンク単位で音声を生成"
                    )
                    generate_btn = gr.Button(
                        "音声生成",
                        variant="primary",
                        size="lg"
                    )

            with gr.Column(scale=1):
                output_audio = gr.Audio(
                    label="生成された音声",
                    type="filepath"
                )

        # サンプルテキスト
        gr.Examples(
            examples=[
                ["こんにちは。今日はいい天気ですね。"],
                ["音声合成技術を使って、テキストから自然な音声を生成できます。"],
                ["[breath]えーと、少し考えさせてください。[breath]はい、わかりました。"],
                ["明日の天気予報です。全国的に晴れる見込みです。"],
            ],
            inputs=[text_input],
            label="サンプルテキスト"
        )

        # イベントハンドラ
        generate_btn.click(
            fn=lambda text, audio, ptext, stream: generate_speech(
                text, audio, ptext, stream, cosyvoice
            ),
            inputs=[text_input, prompt_audio, prompt_text, stream_checkbox],
            outputs=output_audio
        )

    return demo


def main():
    parser = argparse.ArgumentParser(description="Fun-CosyVoice3 日本語 WebUI")
    parser.add_argument(
        "--model_dir",
        type=str,
        default="pretrained_models/Fun-CosyVoice3-0.5B",
        help="モデルディレクトリのパス"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="サーバーポート番号"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="サーバーホスト"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Gradio share リンクを生成"
    )
    args = parser.parse_args()

    # モデルの読み込み
    model_path = os.path.join(os.path.dirname(__file__), args.model_dir)
    if not os.path.exists(model_path):
        print(f"エラー: モデルが見つかりません: {model_path}")
        print("python download_model.py を実行してモデルをダウンロードしてください")
        sys.exit(1)

    cosyvoice = load_model(model_path)

    # UI の作成と起動
    demo = create_ui(cosyvoice)

    print(f"\nWebUI を起動中...")
    print(f"URL: http://{args.host}:{args.port}")

    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share
    )


if __name__ == "__main__":
    main()
