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

# IPA-Discord-notifier

IPA（情報処理推進機構）の **「重要なセキュリティ情報」RSS** を定期取得し、新着だけをDiscordチャンネルにWebhookで投稿します。

## 概要
- IPA公式RSS（重要なセキュリティ情報）の定期取得
- リンク／IDで重複判定し、`sent.json` に送信済みを永続化
- GitHub Actions の Secret に保存した Discord Incoming Webhook URL で投稿

## 取得対象RSS
- 重要なセキュリティ情報（IPA）: `https://www.ipa.go.jp/security/alert-rss.rdf`

## 初回実行の挙動（過去分を流さない）
このリポジトリは **初回実行時に過去分を投稿しません**。

- `sent.json` が存在しない、または中身が空（`[]`）の場合
  - 現時点のRSS全件を「送信済み」として `sent.json` に保存して終了
  - Discordへの投稿は行いません

以降の実行では、RSSに追加された新着分だけ投稿されます。

## セットアップ（GitHub Actions）
1. Repository Settings → Secrets and variables → Actions を開く
2. リポジトリシークレットを追加
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: DiscordのWebhook URL

3. Actionsタブでワークフローを有効化（促された場合）
4. 手動実行する場合
   - Actions → "IPA RSS to Discord" → Run workflow

## リセット（もう一度「初回扱い」にしたい場合）
初回の挙動（投稿せずに `sent.json` を初期化）をやり直したい場合は、次のいずれかを行ってからワークフローを実行してください。

- `sent.json` を `[]` に戻してコミットする
- `sent.json` を削除してコミットする

その次の実行からは、新着だけ投稿されます。

## 補足
- ワークフローは15分ごと（UTC）に実行されます。スケジュールを変えたい場合は `.github/workflows/ipa.yml` を編集してください。
- 同じアイテムを再投稿しないよう、`sent.json` をワークフローがコミットします。
- Webhook URL はコミットせず、必ず GitHub Secrets に保持してください。