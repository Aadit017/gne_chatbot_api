const express = require('express')
const bodyParser = require('body-parser')
const fs = require('fs')
const { makeid } = require('./makeHash')
const { log } = require('console')
const PORT = 3000
const app = express()

app.use(bodyParser.json())

const jsonDataBase = "./db.json" // json file being used as a databaselet data=[] // using this array just to store userId
// let database = JSON.parse(fs.readFileSync(jsonDataBase))
let obj = {
  table: []
};
// let json = JSON.stringify(obj)

const tablePush = (_id, _question, _answer) => {
  obj.table.push({
    id: _id,
    question: _question,
    answer: _answer
  })
  // json = JSON.stringify(obj)
}

function saveDatabase() {
  fs.writeFileSync(jsonDataBase, JSON.stringify(obj), 'utf-8');
}

app.get('/data', (req, res) => {
  // res.json(database.data)
  fs.readFile("./db.json", "utf8", (err, jsonString) => {
    if (err) {
      console.log("File read failed:", err);
      return;
    }
    console.log(JSON.parse(jsonString));
    res.send(jsonString)
  });
});

app.post('/data', (req, res) => {
  const newData = req.body
  tablePush(makeid(10), newData.question, newData.answer)
  saveDatabase()
})

app.get('/', (req, res) => {
  res.sendFile('index.html', { root: __dirname }) // comment this line during production 
})

app.listen(PORT, () => {
  console.log(`The server is running at the port ${PORT}`);
})
