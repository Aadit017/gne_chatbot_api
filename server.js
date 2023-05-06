const express = require('express')
const bodyParser=require('body-parser')
const PORT=3000
const app=express()

app.use(bodyParser.json())
let data=[]
app.get('/data', (req, res) => {
    res.json(data);
  });

app.get('/', (req, res) => {
    res.sendFile('index.html', {root: __dirname })
    // res.send(`<h1>PORT ${PORT} </h1>`)
  })

app.listen(PORT,()=>{
    console.log(`The server is running at the port ${PORT}`);
})
