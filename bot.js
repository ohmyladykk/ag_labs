async function sendLine() {
    // 宛先を指定して送信する「プッシュメッセージ」エンドポイント
    const url = "https://api.line.me/v2/bot/message/push";

    // 環境変数からチャネルアクセストークンとユーザーIDを取得
    const token = process.env.LINE_CHANNEL_ACCESS_TOKEN;
    const userId = process.env.LINE_USER_ID;

    if (!token) {
        console.error("エラー: LINE_CHANNEL_ACCESS_TOKEN の環境変数が設定されていません。");
        return;
    }
    if (!userId) {
        console.error("エラー: LINE_USER_ID の環境変数が設定されていません。宛先を指定するためのユーザーIDが必要です。");
        return;
    }

    const headers = {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
    };

    const now = new Date();
    // 日本時間にあわせて成形
    const timeString = now.toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
    const msg = `【勤怠連絡】\nおはようございます。本日は在宅勤務(テレワーク)にて業務を開始いたします。\n現在時刻: ${timeString}\nよろしくお願いいたします。`;

    // LINE Messaging API 用のJSONフォーマット（"to" でユーザーIDを指定）
    const body = JSON.stringify({
        to: userId,
        messages: [
            {
                type: "text",
                text: msg
            }
        ]
    });

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: body
        });

        if (!response.ok) {
            const errorDetails = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, details: ${errorDetails}`);
        }
        console.log("LINE notification sent successfully via Messaging API (Push).");
    } catch (error) {
        console.error(`Failed to send LINE notification: ${error.message}`);
        if (error.cause) console.error("Cause:", error.cause);
    }
}

sendLine();

