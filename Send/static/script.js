async function generateText() {
    const name = document.getElementById('name').value;
    const age = document.getElementById('age').value;
    const gender = document.getElementById('gender').value;
    const interest = document.getElementById('interest').value;
    const topic = document.getElementById('topic').value;
    const minWords = document.getElementById('minWords').value;

    const response = await fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            age: age,
            gender: gender,
            interest: interest,
            topic: topic,
            minWords: minWords,
        }),
    });

    const result = await response.json();
    if (response.ok) {
        document.getElementById('output-text').textContent = result.text;
    } else {
        console.error(result.error);
        alert("Error: " + result.error);
    }
}