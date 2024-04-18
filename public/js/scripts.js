document.getElementById('commentForm').addEventListener('submit', function(event) {
    
    event.preventDefault(); 
    var comment = document.getElementById('commentInput').value;

    fetch('/classify', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ comment: comment })
    })
    .then(response => response.json())
    .then(data => {
        // Update UI with classification result
        document.getElementById('classificationResult').innerText = data.result;
    })
    .catch(error => console.error('Error:', error));
});
