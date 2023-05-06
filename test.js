// File made entirely for testing , not to be used in production
fetch("http://localhost:3000/data", {
  method: "POST",
  body: JSON.stringify({
    question:"who are in paris",
    answer:"niggas"
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
