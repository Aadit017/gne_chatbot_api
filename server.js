const express = require('express')
const bodyParser=require('body-parser')
const fs=require('fs')
const PORT=3000
const app=express()

app.use(bodyParser.json())
let data=[]
app.get('/data', (req, res) => {
    res.json(data);
  });

app.post('/data',(req,res)=>{
    const newData=req.body 
    console.log(`Post Method \n stuff recieved ${newData.userId}`);
    data.push(newData.userId)
})

app.get('/', (req, res) => {
    // res.sendFile('index.html', {root: __dirname })
    res.json(data)
  })
app.listen(PORT,()=>{
    console.log(`The server is running at the port ${PORT}`);
})
