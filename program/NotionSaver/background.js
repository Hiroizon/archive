chrome.runtime.onInstalled.addListener(function() {
    chrome.runtime.openOptionsPage();
  });
  
   chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === "saveToNotion") {
      sendDataToNotion(request.data, request.apiKey, request.databaseId)
       .then(response => sendResponse(response))
        .catch(error => sendResponse({ success: false, error: error.message }));
       return true;
      }
    });
  
    async function sendDataToNotion(data, apiKey, databaseId) {
        const notionUrl = 'https://api.notion.com/v1/pages';
       const headers = {
             'Authorization': `Bearer ${apiKey}`,
             'Content-Type': 'application/json',
             'Notion-Version': '2022-06-28'
         };
  
       const body = {
           parent: { database_id: databaseId },
           properties: {
               "タイトル": { title: [{ text: { content: data.title } }] },
               "URL": { url: data.url },
               "日時": { date: { start: data.date } },
               "感想": { rich_text: [{ text: { content: data.comment } }] },
           }
       };
        try {
            const response = await fetch(notionUrl, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(body)
             });
  
            if (!response.ok) {
              const responseBody = await response.text();
                 let parsedBody;
              try {
                   parsedBody = JSON.parse(responseBody);
                } catch (e) {
                     console.error("JSON parse error:", e);
                    throw new Error(`Notion API request failed with status ${response.status}. Response body could not be parsed: ${responseBody}`);
                  }
              console.error("Notion API error:", parsedBody);
              throw new Error(`Notion API request failed with status ${response.status}: ${parsedBody.message || responseBody}`);
              }
          return { success: true };
        } catch (error) {
             console.error("Error sending data to Notion:", error);
              throw new Error(`Notion API request failed : ${error.message}`);
        }
    }