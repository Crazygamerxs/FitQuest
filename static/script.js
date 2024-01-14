document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_user_info')
        .then(response => response.json())
        .then(data => {
            displayLeaderboard(data);
        })
        .catch(error => console.error('Error:', error));
});

function displayLeaderboard(leaderboard) {
    var leaderboardElement = document.getElementById('leaderboard');
    leaderboardElement.innerHTML = '';

    for (var i = 0; i < leaderboard.length; i++) {
        var li = document.createElement('li');
        li.textContent = leaderboard[i].name + ' - ' + leaderboard[i].number;
        leaderboardElement.appendChild(li);
    }
}

function clearLeaderboard() {
    fetch('/clear_leaderboard')
        .then(response => response.json())
        .then(data => {
            displayLeaderboard(data);
        })
        .catch(error => console.error('Error:', error));
}
