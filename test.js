// File made entirely for testing , not to be used in production
fetch("http://localhost:3000/data", {
  method: "POST",
  body: JSON.stringify({
    question:"what is your name",
    answer:"Aadit Singh Bagga"
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
