const express = require('express')
const bodyParser=require('body-parser')
const PORT=3000
const app=express()


app.get('/', (req, res) => {
    res.send('working')
  })
  
app.listen(PORT,()=>{
    console.log(`The server is running at the port ${PORT}`);
})
