document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    window.location.href = 'homepage.html';
});

function loadPage(page) {
    fetch(page)
        .then(response => response.text())
        .then(data => {
            document.getElementById('content').innerHTML = data;
        });
}

function showNewCampaign() {
    document.getElementById('campaignContent').innerHTML = `
        <div class="form-container">
            <h2>New Campaign</h2>
            <form>
                <label for="targetDomain">Target Domain Name:</label>
                <input type="text" id="targetDomain" name="targetDomain" required>
                <label for="campaignList">Campaigns:</label>
                <select id="campaignList" name="campaignList">
                    <!-- Options will be added here dynamically -->
                </select>
                <button type="submit">Create Campaign</button>
            </form>
            <button class="upload-btn" onclick="uploadCSV()">Upload CSV</button>
            <input type="file" id="fileInput" style="display:none" accept=".csv">
        </div>
    `;
    document.getElementById('fileInput').addEventListener('change', handleFileUpload);
}

function showViewCampaign() {
    document.getElementById('campaignContent').innerHTML = `
        <div class="form-container">
            <h2>View Campaign</h2>
            <form>
                <label for="targetDomain">Target Domain Name:</label>
                <input type="text" id="targetDomain" name="targetDomain" required>
                <label for="campaignList">Campaigns:</label>
                <select id="campaignList" name="campaignList">
                    <!-- Options will be added here dynamically -->
                </select>
                <button type="submit">View Campaign</button>
            </form>
        </div>
    `;
}

function uploadCSV() {
    document.getElementById('fileInput').click();
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
        const content = e.target.result;
        console.log(content); // Process CSV content
    };
    reader.readAsText(file);
}

function loadPage(page) {
    fetch(page)
        .then(response => response.text())
        .then(data => {
            document.getElementById('content').innerHTML = data;
        });
}

function getGeolocationAndRedirect() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const url = `your_activity.html?lat=${latitude}&lon=${longitude}`;
            window.location.href = url;
        }, function(error) {
            console.error("Error getting geolocation: ", error);
            // Handle the error case here if needed
        });
    } else {
        console.error("Geolocation is not supported by this browser.");
        // Handle the error case here if needed
    }
}
