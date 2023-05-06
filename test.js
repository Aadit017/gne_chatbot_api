// File made entirely for testing , not to be used in production
fetch("http://localhost:3000/users", {
  method: "POST",
  body: JSON.stringify({
      "name": "singh",
      "email": "johndoe@example.com",
      "age": 35
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
