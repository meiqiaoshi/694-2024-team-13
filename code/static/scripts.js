document.getElementById('search-btn').addEventListener('click', function() {
    let query = document.getElementById('search-box').value;
    currentPage = 1; // Reset currentPage to 1 for new searches
    fetch('/search', {
        method: 'POST',
        // Ensure the headers part is set with the correct Content-Type
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        // Encode the query string directly since we are not using a <form> element
        body: 'query=' + encodeURIComponent(query)
    })
    .then(response => response.json())
    .then(data => {
        if (Object.keys(data).length > 0) { // Check if the data object is not empty
            // Call a function to process the data and update the DOM
            displayResults(data, true);
        }
        // If data is empty, do nothing
    }).catch(error => {
        // Display any errors in the console
        console.error('Error:', error);
    });
});

function displayResults(data, clearContents) {
    let peopleContainer = document.getElementById('people-container');
    let tweetsContainer = document.getElementById('tweets-container');

    if (clearContents) {
        peopleContainer.innerHTML = '';
        tweetsContainer.innerHTML = '';
    }

    if (data.people) {
        // For each person, create a new div element and add it to peopleContainer
        data.people.forEach(function(person) {
            let personDiv = document.createElement('div');
            personDiv.className = 'person';
            personDiv.innerHTML = `
                <a href="${person.link}" target="_blank" style="text-decoration: none; color: inherit;">
                    <h4>${person.name}</h4>
                    <p>${person.description}</p>
                </a>`;
            peopleContainer.appendChild(personDiv);
        });
    }

    if (data.tweets) {
        // For each tweet, create a new div element and add it to tweetsContainer
        data.tweets.forEach(function(tweet) {
            let tweetDiv = document.createElement('div');
            tweetDiv.className = 'tweet';
            tweetDiv.innerHTML = `
                <a href="${tweet.link}" target="_blank" style="text-decoration: none; color: inherit;">
                    <h4>${tweet.user}</h4>
                    <p>${tweet.content}</p>
                    <span>${tweet.timestamp}</span>
                </a>`;
            tweetsContainer.appendChild(tweetDiv);
        });
    }
}

// ...
// Current page and expected page size for loading tweets
let currentPage = 1;
const pageSize = 10;  // Assuming 10 tweets are loaded per page

// Listen for scroll events to load more tweets
window.addEventListener('scroll', () => {
    // Check if the user has scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        loadMoreTweets(currentPage);
    }
});

function loadMoreTweets(page) {
    currentPage++;
    fetch(`/search?query=${encodeURIComponent(document.getElementById('search-box').value)}&page=${currentPage}&pageSize=${pageSize}`, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
        if (data && (data.people.length > 0 || data.tweets.length > 0)) {
            displayResults(data, false); // Append new results to existing content
        }
    }).catch(error => {
        console.error('Error loading more tweets:', error);
    });
}



// The displayResults function remains unchanged
// ...
