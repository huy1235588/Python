const { Builder, By, Key, until } = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');

function calculateDaysBetweenDates(date1, date2) {
    // Chuyển đổi các đối tượng Date thành milliseconds
    const date1_ms = new Date(date1).getTime();
    const date2_ms = new Date(date2).getTime();

    // Tính khoảng cách giữa hai ngày (chênh lệch thời gian)
    const difference_ms = Math.abs(date2_ms - date1_ms);

    // Chuyển đổi khoảng cách từ milliseconds thành số ngày
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    const difference_days = Math.floor(difference_ms / millisecondsPerDay);

    return difference_days;
}

(async function example() {
    const link_game8 = "https://game8.co/games/Genshin-Impact/archives/297500"
    const link_vietnamonline = "https://www.vietnamonline.com/current-time.html"
    const file_html_path = "e:/Project/Python/calendar/web/ha.html"

    let options = new chrome.Options();
    options.addArguments("headless"); // Chạy ở chế độ headless

    let driver = await new Builder()
        .forBrowser('chrome')
        .setChromeOptions(options)
        .build();

    try {
        await driver.get(link_game8);

        let current_phare = await driver.findElement(By.id("hl_1"));
        current_phare = (await current_phare.getText());

        if (current_phare.includes("Phase 1")) {
            let phase_2_datetime_text = await driver.findElement(By.xpath('//*[@width="60%"]'));
            phase_2_datetime_text = (await phase_2_datetime_text.getText()).split("-")[0];

            await driver.get(link_vietnamonline);
            let current_datetime_text = await driver.findElements(By.className("tb-cell"));
            current_datetime_text = (await current_datetime_text[5].getText());

            const daysBetween = calculateDaysBetweenDates(current_datetime_text, phase_2_datetime_text)
            if (daysBetween >= 4) {
                // console.log(daysBetween);
                if (typeof window !== 'undefined') {
                    window.open(file_html_path);
                  }
            }
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
    finally {
        await driver.quit();
    }
})();