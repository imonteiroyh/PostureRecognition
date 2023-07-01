const express = require('express');

const app = express();

app.use(express.static('public'))

app.get('/', (req,res) => {
    res.sendFile(__dirname + '/index.html');
})

app.listen(8000, (req,res) => {
    console.log("Servidos rodando na porta 8000");
})