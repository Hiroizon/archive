document.addEventListener('DOMContentLoaded', function() {
    loadSettings();
    document.getElementById('saveSettings').addEventListener('click', saveSettings);
});

function loadSettings() {
    chrome.storage.local.get(['notionApiKey', 'notionDatabaseId'], function(items) {
      document.getElementById('notionApiKey').value = items.notionApiKey || '';
      document.getElementById('notionDatabaseId').value = items.notionDatabaseId || '';
    });
  }

function saveSettings() {
    const apiKey = document.getElementById('notionApiKey').value;
    const databaseId = document.getElementById('notionDatabaseId').value;

    chrome.storage.local.set({
        'notionApiKey': apiKey,
        'notionDatabaseId': databaseId
    }, function() {
        document.getElementById('status').textContent = 'Settings saved.';
        setTimeout(() => {
            document.getElementById('status').textContent = '';
        }, 2000);
    });
}