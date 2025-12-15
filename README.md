# IPA-Discord-notifier

IPA（情報処理推進機構）のRSSフィードを取得し、新着をDiscordチャンネルにWebhookで投稿します。

## 概要
- IPA公式のRSSフィードを定期取得
- リンク／IDで重複判定し、`sent.json` に永続化
- GitHub ActionsのSecretに保存したDiscord Incoming Webhook URLで投稿

## セットアップ（GitHub Actions）
1. Repository Settings → Secrets and variables → Actions を開く
2. リポジトリシークレットを追加
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: DiscordのWebhook URL

3. Actionsタブでワークフローを有効化（促された場合）
4. 手動実行する場合
   - Actions → "IPA RSS to Discord" → Run workflow

## 補足
- ワークフローは15分ごと（UTC）に実行されます。スケジュールを変えたい場合は `.github/workflows/ipa.yml` を編集してください。
- 同じアイテムを再投稿しないよう、`sent.json` をワークフローがコミットします。
- Webhook URLはコミットせず、必ずGitHub Secretsに保持してください。
