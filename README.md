サイトセブン 出玉データ スクレイピングツール

本ツールは サイトセブン（d-deltanet.com） のホール出玉データページから
指定店舗・指定機種の出玉データを自動でスクレイピングしてCSVに保存する Python スクリプトです。
❗️ 注意事項
•本スクリプトは サイトセブン利用規約で禁止されている自動取得行為に該当します。
自己責任で使用してください。

•研究用途・技術習得用に公開しており、商用利用・過度なアクセスは推奨しません。

•アカウント凍結や法的リスクについては一切責任を負いません。
⸻

📌 主な機能

✅ Cookie認証による自動ログイン
✅ 指定店舗ページへの自動遷移
✅ 各機種の出玉データ取得
✅ 日付・曜日付きでCSVへ追記保存（機種ごとにファイル分割）
✅ Seleniumのバージョン管理不要（chromedriver-autoinstaller使用）
✅ VPS上で cron による定期実行に対応済み

⸻

💻 対応環境
•Python 3.9 以上推奨
•Google Chrome（最新版推奨）
•対応OS：Windows / Mac / Linux / VPS（ConoHa VPS等）

⸻

🛠 使用ライブラリ
selenium
pandas
chromedriver-autoinstaller
pickle（標準ライブラリ）
datetime（標準ライブラリ）

⚙️ 設定内容

1️⃣ Cookieファイル（cookies_pc.pkl）
•手動ログイン後に取得した Cookie を pickle 形式で保存しておきます。
•これによりログイン画面をスキップして直接データ取得可能。

address_text = "茨城県常総市新井木町字江畑３７－１"  # 店舗住所でホールページを特定

machines = {
    "ゴーゴージャグラー３": "gogojuggler3.csv",
    "キングハナハナ-30": "kinghanahana.csv",
    "SアイムジャグラーＥＸ": "SimJuggler.csv",
    "ハナハナホウオウ～天翔～-30": "hououhanahana.csv",
    "ジャグラーガールズSS": "jugglergirls.csv",
    "マイジャグラーV": "myjuggler5.csv",
    "ミスタージャグラー": "misterjuggler.csv",
    "ハッピージャグラーＶＩＩＩ": "happyjuggler8.csv"
}

🚀 実行方法

# 例）毎日 23:30 に実行（日本時間）
30 23 * * * /path/to/venv/bin/python /path/to/your_script_name.py >> /path/to/logfile.log 2>&1

✅ VPSで毎日自動収集＆CSV更新中
✅ CSVは WinSCP 等でローカルにDLして分析・活用

📂 出力ファイル例
•機種ごとに CSV ファイル出力
（例）gogojuggler3.csv
CSV カラム：
日付
曜日
台番号
総スタート
BB回数
RB回数
合成確率

✅ 運用例
•VPS（ConoHa VPS）上で cron により毎日 23:30 に定期実行
•出力CSVを WinSCP でローカルにDL → pandasでデータ分析
