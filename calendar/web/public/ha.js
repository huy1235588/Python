
const button = document.getElementById('btn');

button.addEventListener('click', function () {
    button.classList.add('clicked');

    const data = {
        varrient: "true",
        timestamp: new Date().toLocaleDateString(),
        elapse_date: "0"
    };

    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.text())
        .then(data => {
            console.log(data);

            // Send request to shutdown server
            return fetch('/shutdown', {
                method: 'POST'
            });
        })

        .then(response => response.text())
        .then(data => {
            console.log(data);
        })

        .catch(error => {
            console.error('Error:', error);
        });
});

