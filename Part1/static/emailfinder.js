// emailfinder.js

document.getElementById('fetch-type').addEventListener('change', (event) => {
    const fetchType = event.target.value;
    if (fetchType === 'single') {
        document.getElementById('single-inputs').style.display = 'block';
        document.getElementById('bulk-inputs').style.display = 'none';
    } else if (fetchType === 'bulk') {
        document.getElementById('single-inputs').style.display = 'none';
        document.getElementById('bulk-inputs').style.display = 'block';
    }
});

document.getElementById('fetch-emails').addEventListener('click', () => {
    const names = document.getElementById('names').value.split('\n').map(name => name.trim()).filter(name => name);
    const domain = document.getElementById('domain').value.trim();
    fetch('/fetch_emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fetch_type: 'single', domain, names })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('emails').innerText = data.emails.join('\n');
    })
    .catch(error => {
        console.error('Error fetching emails:', error);
        // Display error message to user if necessary
    });
});

document.getElementById('fetch-emails-bulk').addEventListener('click', () => {
    const bulkData = document.getElementById('bulk-data').value.trim();
    let emailData;
    try {
        emailData = JSON.parse(bulkData);
    } catch (error) {
        console.error('Invalid JSON format for bulk data:', error);
        // Display error message to user if necessary
        return;
    }
    fetch('/fetch_emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fetch_type: 'bulk', email_data: emailData })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const emails = data.valid_emails.flatMap(entry => entry.valid_emails);
        document.getElementById('emails').innerText = emails.join('\n');
    })
    .catch(error => {
        console.error('Error fetching emails in bulk:', error);
        // Display error message to user if necessary
    });
});

document.getElementById('scrape-emails').addEventListener('click', () => {
    const urls = document.getElementById('urls').value.split('\n').map(url => url.trim()).filter(url => url);
    fetch('/scrape_emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urls })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('emails').innerText = data.emails.join('\n');
    })
    .catch(error => {
        console.error('Error scraping emails:', error);
        // Display error message to user if necessary
    });
});

document.getElementById('check-emails').addEventListener('click', () => {
    fetch('/check_emails', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('live-emails').innerText = data.live_emails.join('\n');
        document.getElementById('dead-emails').innerText = data.dead_emails.join('\n');

        renderCharts(data.live_emails, data.dead_emails);
    })
    .catch(error => {
        console.error('Error checking emails:', error);
        // Display error message to user if necessary
    });
});

function renderCharts(liveEmails, deadEmails) {
    const ctxBar = document.getElementById('barChart').getContext('2d');
    const ctxPie = document.getElementById('pieChart').getContext('2d');

    // Bar chart showing number of emails fetched domain wise
    const liveCount = liveEmails.reduce((acc, email) => {
        const domain = email.split('@')[1];
        acc[domain] = (acc[domain] || 0) + 1;
        return acc;
    }, {});

    const deadCount = deadEmails.reduce((acc, email) => {
        const domain = email.split('@')[1];
        acc[domain] = (acc[domain] || 0) + 1;
        return acc;
    }, {});

    const domains = Array.from(new Set([...Object.keys(liveCount), ...Object.keys(deadCount)]));

    new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: domains,
            datasets: [{
                label: 'Live Emails',
                data: domains.map(domain => liveCount[domain] || 0),
                backgroundColor: '#36a2eb'
            }, {
                label: 'Dead Emails',
                data: domains.map(domain => deadCount[domain] || 0),
                backgroundColor: '#ff6384'
            }]
        }
    });

    // Pie chart showing live vs dead emails
    new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: ['Live Emails', 'Dead Emails'],
            datasets: [{
                data: [liveEmails.length, deadEmails.length],
                backgroundColor: ['#36a2eb', '#ff6384']
            }]
        }
    });
}
