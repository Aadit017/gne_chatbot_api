const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const port = 3000;

// Configure body-parser to handle JSON data
app.use(bodyParser.json());

// Define the path to the JSON file
const dbFilePath = './db.json';

// Read the JSON file and parse its contents
let database = JSON.parse(fs.readFileSync(dbFilePath));

// Define a function to save the database to the file
function saveDatabase() {
  fs.writeFileSync(dbFilePath, JSON.stringify(database, null, 2));
}

// Define routes for your API
app.get('/users', (req, res) => {
  res.json(database.users);
});

app.post('/users', (req, res) => {
  const newUser = req.body;
  const userId = Object.keys(database.users).length + 1;
  newUser.id = userId;
  database.users[userId] = newUser;
  saveDatabase();
  res.json(newUser);
});

app.get('/users/:id', (req, res) => {
  const userId = req.params.id;
  const user = database.users[userId];
  if (user) {
    res.json(user);
  } else {
    res.status(404).send('User not found');
  }
});

app.put('/users/:id', (req, res) => {
  const userId = req.params.id;
  const user = database.users[userId];
  if (user) {
    const updatedUser = { ...user, ...req.body };
    database.users[userId] = updatedUser;
    saveDatabase();
    res.json(updatedUser);
  } else {
    res.status(404).send('User not found');
  }
});

app.delete('/users/:id', (req, res) => {
  const userId = req.params.id;
  const user = database.users[userId];
  if (user) {
    delete database.users[userId];
    saveDatabase();
    res.json(user);
  } else {
    res.status(404).send('User not found');
  }
});

app.get("/",(req,res)=>{
  res.send("working?")
})
// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
