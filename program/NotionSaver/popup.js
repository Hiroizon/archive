document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('saveButton').addEventListener('click', saveToNotion);
});

async function saveToNotion() {
    console.log('送信ボタンがクリックされました');
    const comment = document.getElementById('comment').value;
    const status = document.getElementById('status');
    const errorContainer = document.getElementById('error-container');
    status.textContent = "保存中...";
    errorContainer.textContent = ''; // エラーメッセージをクリア

    // Notion APIキーとデータベースIDをストレージから取得
    const storedData = await chrome.storage.local.get(['notionApiKey', 'notionDatabaseId']);
    console.log('取得したデータ:', storedData);
    const notionApiKey = storedData.notionApiKey;
    const notionDatabaseId = storedData.notionDatabaseId;

    if (!notionApiKey || !notionDatabaseId) {
        console.log('APIキーとデータベースIDのチェック');
        status.textContent = "Notion APIキーとデータベースIDを設定してください。拡張機能の設定画面を開き設定してください。";
        return;
    }

    chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
        if (!tabs || tabs.length === 0) {
            console.error('アクティブなタブが見つかりません');
            status.textContent = "アクティブなタブが見つかりません。";
            return;
        }
        const tab = tabs[0];
        const title = tab.title;
        const url = tab.url;
        const date = new Date().toISOString().replace("Z", "+00:00");
        // const formatter = new Intl.DateTimeFormat('en-CA', { // ISO8601に近い形式を指定
        //     year: 'numeric',
        //     month: '2-digit',
        //     day: '2-digit',
        //     hour: '2-digit',
        //     minute: '2-digit',
        //     second: '2-digit',
        //     timeZone: 'Asia/Tokyo',
        // });

        // const date = `${formatter.format(new Date()).replace(/[/]/g, '-').replace(/(\s|\u3000)/g, 'T')}+09:00`;

        const data = {
            "title": title,
            "url": url,
            "date": date,
            "comment": comment
        };
        console.log('data.date:', data.date);

        try {
            console.log('バックグラウンドに送信');
            const response = await chrome.runtime.sendMessage({
                action: "saveToNotion",
                data: data,
                apiKey: notionApiKey,
                databaseId: notionDatabaseId
            });
            if (response.success) {
                status.textContent = "記事がNotionに保存されました！";
            } else {
                status.textContent = "記事の保存に失敗しました。";
                errorContainer.textContent = response.error;
            }
        } catch (error) {
            console.error("Error sending data to Notion:", error);
            status.textContent = "記事の保存に失敗しました。";
            errorContainer.textContent = error.message;
        }
    });
}