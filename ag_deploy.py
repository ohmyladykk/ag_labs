import os
import subprocess
import datetime

def deploy():
    print("🚀 AG Labs システム：GitHubへの一斉デプロイを開始します...")
    
    # 現在の時刻をコミットメッセージにする（社長の手間を省く！）
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"CEO Update: {now} (Auto-deployed by Antigravity)"
    
    try:
        # 1. 変更をすべてステージング
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. コミット（メッセージ自動生成）
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # 3. GitHubへプッシュ！
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("\n✅ 【完全勝利】GitHubへのアップロードが完了しました！")
        print("🌐 社長のサイトはこちら:")
        # GitHub PagesのURLを推測して表示（リポジトリ名から）
        print("https://ohmyladykk.github.io/ag_labs2/")
        
    except subprocess.CalledProcessError as e:
        print(f"\n⚠️ エラー発生: 変更がないか、GitHubとの接続に問題があります。")
        print(f"詳細: {e}")

if __name__ == "__main__":
    deploy()
