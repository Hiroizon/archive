document.getElementById('runScript').addEventListener('click', () => {
    const selectedSchedule = document.getElementById('scheduleSelect').value;
    const customMessage = document.getElementById('messageSelect').value;

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: runAutoFillScript,
            args: [selectedSchedule, customMessage] // 選択した値を渡す
        });
    });
});

function runAutoFillScript(selectedSchedule, customMessage) {
    function isWeekday(dateTd) {
        if (dateTd.querySelector('.saturday') || dateTd.querySelector('.holiday')) {
            return false; // 週末または祝日
        }
        return true; // 平日
    }

    const rows = document.querySelectorAll('tbody > tr');
    rows.forEach((row, index) => {
        const dateTd = row.querySelector('.htBlock-vrCalendarTable_day');
        if (dateTd && isWeekday(dateTd)) {
            // スケジュールパターンの選択
            if (selectedSchedule !== "none") {
                const scheduleSelect = row.querySelector('.htBlock-selectmenu.htBlock-selectmenu-fix-width[name="requested_schedule_pattern_list"]');
                if (scheduleSelect) {
                    const scheduleOption = scheduleSelect.querySelector(`option[value="${selectedSchedule}"]`);
                    if (scheduleOption) {
                        scheduleSelect.value = scheduleOption.value; // 選択したスケジュールを適用
                    }
                }
            }

            // 勤務日種別の選択
            const workingDayTypeSelect = row.querySelector('.htBlock-selectmenu[name="requested_working_day_type_list"]');
            if (workingDayTypeSelect) {
                workingDayTypeSelect.value = "1"; // 「平日」を選択
            }

            // 申請メッセージの設定
            const messageRow = rows[index + 2]; // 申請メッセージは2つ次の行にある
            const remarkInput = messageRow.querySelector('input[name="remark_list"]');
            if (remarkInput && customMessage) {
                remarkInput.value = customMessage; // テキストボックスの値を適用
            }
        }
    });
}

// ページからスケジュールパターンを取得し、ドロップダウンリストを生成する関数
function populateScheduleDropdown() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: getSchedulePatterns,
        }, (results) => {
            if (results && results[0] && results[0].result) {
                const schedulePatterns = results[0].result;
                const scheduleSelect = document.getElementById('scheduleSelect');
                scheduleSelect.innerHTML = '<option value="none">-- 選択してください --</option>';
                schedulePatterns.forEach(pattern => {
                    const option = document.createElement('option');
                    option.value = pattern.value;
                    option.textContent = pattern.text;
                    scheduleSelect.appendChild(option);
                });
            }
        });
    });
}

// ページからスケジュールパターンを取得する関数
function getSchedulePatterns() {
    const scheduleSelect = document.querySelector('.htBlock-selectmenu.htBlock-selectmenu-fix-width[name="requested_schedule_pattern_list"]');
    if (scheduleSelect) {
        return Array.from(scheduleSelect.options).map(option => ({
            value: option.value,
            text: option.textContent
        }));
    }
    return [];
}

// ポップアップが開かれたときにスケジュールパターンを取得して表示
document.addEventListener('DOMContentLoaded', populateScheduleDropdown);
