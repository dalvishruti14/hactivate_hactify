function getResponse() {
    const message = document.getElementById('message').value;

    fetch('/respond', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: message })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').value = data.response;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while fetching the response.');
    });
}
