const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

// Prepare the form data
const form = new FormData();
form.append('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5ODMzMTg0LCJpYXQiOjE3Mjk0MjgwNzgsImp0aSI6ImIwM2U4NTliMzk1NjQyYjM4YWNhMTJmZTVjYTU2OWM5IiwidXNlcl9pZCI6N30.R9wS5Hscp5CegiKIbDfPgzFyb3oy1rRDNNNhvRKKAfs'); // Add token to form
form.append('image', fs.createReadStream("C:\\Users\\Pritimaya Sahoo\\OneDrive\\Pictures\\IMG-20221216-WA0005.jpg")); // Path to your image

// Send the request
axios.post('http://127.0.0.1:8000/save/', form, {
  headers: {
    ...form.getHeaders(),
  },
})
  .then(response => {
    console.log('Success:', response.data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
