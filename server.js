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
app.get('/faqs', (req, res) => {
  res.json(database.faqs);
});

app.post('/faqs', (req, res) => {
  const newUser = req.body;
  const userId = Object.keys(database.faqs).length + 1;
  newUser.id = userId;
  database.faqs[userId] = newUser;
  saveDatabase();
  res.json(newUser);
});

app.get('/faqs', (req, res) => {
  const faqs = Object.values(database.faqs).map(({ question, answer }) => ({ question, answer }));
  res.json(faqs);
});

app.get('/faq', (req, res) => {
  const faqs = Object.values(database.faqs).map(({ question, answer }) => ({ question, answer }));
  res.json(faqs);
});

app.get('/faqs/:id', (req, res) => {
  const userId = req.params.id;
  const user = database.faqs[userId];
  if (user) {
    res.json(user);
  } else {
    res.status(404).send('User not found');
  }
});

app.put('/faqs/:id', (req, res) => {
  const userId = req.params.id;
  const user = database.faqs[userId];
  if (user) {
    const updatedUser = { ...user, ...req.body };
    database.faqs[userId] = updatedUser;
    saveDatabase();
    res.json(updatedUser);
  } else {
    res.status(404).send('User not found');
  }
});

app.delete('/faqs/:question', (req, res) => {
  const question = req.params.question;
  const faqToDelete = Object.values(database.faqs).find(faq => faq.question === question);
  if (faqToDelete) {
    const faqIdToDelete = faqToDelete.id;
    delete database.faqs[faqIdToDelete];
    saveDatabase();
    res.json(faqToDelete);
  } else {
    res.status(404).send('FAQ not found');
  }
});


app.get("/",(req,res)=>{
  res.send("working?")
})
// Start the server
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
