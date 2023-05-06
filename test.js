fetch("http://localhost:3000/data", {
  method: "POST",
  body: JSON.stringify({
    userId: 23
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
});