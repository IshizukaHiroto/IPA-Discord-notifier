# IPA-Discord-notifier

IPA（情報処理推進機構）の **「重要なセキュリティ情報」RSS** を定期取得し、新着だけを Discord チャンネルに Webhook で投稿します。

## 概要
- IPA 公式 RSS（重要なセキュリティ情報）を15分ごと（UTC）に取得
- リンク/IDベースで重複判定し、送信済みは `sent.json` に保存
- ワークフローが `sent.json` を自動コミットし、同じアイテムを再投稿しない

## 取得対象 RSS
- 重要なセキュリティ情報（IPA）: `https://www.ipa.go.jp/security/alert-rss.rdf`

## 動作仕様
- 初回実行時に `sent.json` が空なら、RSS全件を「送信済み」として保存し、投稿は行わない（過去分を流さない）。
- 1回の実行で送る上限は `MAX_POST_PER_RUN`（既定 20）。
- Discord には埋め込みで送信し、本文内の `@everyone` 等は無効化済み。

## 必要な環境変数
- `DISCORD_WEBHOOK_URL`（必須）: Discord Incoming Webhook URL。
- `MAX_POST_PER_RUN`（任意）: 1回に投稿する最大件数。既定 `20`。
- `HTTP_TIMEOUT_SEC`（任意）: Webhook 送信のタイムアウト秒。既定 `20`。

## GitHub Actions セットアップ
1. Repository Settings → Secrets and variables → Actions を開く。
2. シークレットを追加  
   - Name: `DISCORD_WEBHOOK_URL`  
   - Value: Discord の Webhook URL
3. Actions タブでワークフローを有効化（促された場合）。
4. 手動実行する場合: Actions → “IPA RSS to Discord” → “Run workflow”。

## ローカル実行手順（手動テストしたい場合）
1. Python 3.12+ を用意（`python --version` で確認）。
2. 依存をインストール: `pip install -r requirements.txt`
3. Webhook を設定  
   - `.env.example` を `.env` にコピーして URL を差し替える、または `export DISCORD_WEBHOOK_URL=...`
4. 必要なら上限を絞る: `export MAX_POST_PER_RUN=1` など。
5. 実行: `python ipa_to_discord.py`  
   - 実行後、送信済みは `sent.json` に追記されます（ローカルでは自動コミットはされません）。

## 重複防止の確認例
- テスト用 Webhook を用意した上で、`sent.json` の末尾を1件削除してコミット/プッシュ → ワークフローを手動実行すると、その1件だけが投稿されます。続けてもう一度実行すると `posted=0` になり、再投稿されないことを確認できます。

## 補足
- スケジュールを変更したい場合は `.github/workflows/ipa.yml` の `cron` を編集してください。
- Webhook URL をリポジトリにコミットしないでください。必ず Secrets やローカル環境変数で設定してください。
