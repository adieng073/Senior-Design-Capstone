(async function () {
    let tweetsSet = new Set();
    let noChangeCount = 0;
    let previousHeight = 0;

    function extractTweets() {
        const tweetElements = document.querySelectorAll('[data-testid="tweetText"]');
        tweetElements.forEach(el => {
            tweetsSet.add(el.innerText);
        });
    }

    async function autoScroll() {
        while (true) {
            extractTweets();
            window.scrollBy(0, 1000); // Scroll down to load more tweets
            await new Promise(resolve => setTimeout(resolve, 2000)); // Adjust time to wait for loading

            const currentHeight = document.documentElement.scrollHeight;
            if (currentHeight === previousHeight) {
                noChangeCount++;
            } else {
                noChangeCount = 0;
            }

            previousHeight = currentHeight;

            // Stop if no change detected for several attempts
            if (noChangeCount >= 10) {
                console.log("No more tweets loading. Stopping...");
                break;
            }
        }
    }

    console.log("Starting to scrape tweets...");
    await autoScroll();

    // Use a special delimiter to separate each tweet
    const tweetData = Array.from(tweetsSet).join('~~~TWEET_DELIMITER~~~');
    const blob = new Blob([tweetData], { type: 'text/plain' });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "tweets.txt";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    console.log("Tweets saved. Please move the downloaded file to your desired folder.");
})();
