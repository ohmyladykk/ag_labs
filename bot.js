const axios = require('axios');

// GitHubの金庫から「LINEの鍵」だけを取り出す（全員に送るので、社長のIDはもう使いません！）
const TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN;

if (!TOKEN) {
    console.error('エラー: LINE_CHANNEL_ACCESS_TOKEN が設定されていません。');
    process.exit(1);
}

// 魔法①：宛先を「push（個別）」から「broadcast（全員）」に変更！
const url = 'https://api.line.me/v2/bot/message/broadcast';

// 魔法②：宛先（to）の指定を削除して、メッセージ内容だけにする！
const data = {
    messages: [
        {
            type: 'text',
            // ↓ ここに在宅ワークのリンクや、送りたいメッセージを書いてください！
            text: 'おはようございます！今日の在宅ワークのリンクはこちらです！\nhttps://example.com'
        }
    ]
};

// 鍵穴の準備
const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${TOKEN}`
};

// 全員に向けてメッセージを一斉発射！🚀
axios.post(url, data, { headers: headers })
    .then(response => {
        console.log('一斉送信（Broadcast）大成功！全員に手紙を配りました！:', response.data);
    })
    .catch(error => {
        console.error('エラー発生:', error.response ? error.response.data : error.message);
        process.exit(1);
    });