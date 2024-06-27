function generateText() {
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const interest = document.getElementById('interest').value;
    const topic = document.getElementById('topic').value;
    const minWords = document.getElementById('minWords').value;

    const data = {
        name: name,
        age: age,
        gender: gender,
        interest: interest,
        topic: topic,
        minWords: minWords
    };

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output-text').innerText = data.text;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
