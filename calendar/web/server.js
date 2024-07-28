const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;
let server

app.use(bodyParser.json());
app.use(express.static('public'));

app.post('/save', (req, res) => {
    const data = req.body;

    fs.writeFile('D://Project//Python//calendar//json//ha.json', JSON.stringify(data, null, 2), (err) => {
        if (err) {
            console.error(err);
            return res.status(500).send('Error writing to file');
        }
        res.send('Data saved successfully');
    });
});


app.post('/shutdown', (req, res) => {
    res.send('Shutting down server...');
    server.close(() => {
        console.log('Server closed');
        process.exit(0);
    });
});


server = app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
