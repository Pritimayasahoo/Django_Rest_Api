const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

// // Prepare the form data
// const form = new FormData();
// form.append('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5ODMzMTg0LCJpYXQiOjE3Mjk0MjgwNzgsImp0aSI6ImIwM2U4NTliMzk1NjQyYjM4YWNhMTJmZTVjYTU2OWM5IiwidXNlcl9pZCI6N30.R9wS5Hscp5CegiKIbDfPgzFyb3oy1rRDNNNhvRKKAfs'); // Add token to form
// form.append('image', fs.createReadStream("C:\\Users\\Pritimaya Sahoo\\OneDrive\\Pictures\\IMG-20221216-WA0005.jpg")); // Path to your image

// // Send the request
// axios.post('http://127.0.0.1:8000/save/', form, {
//   headers: {
//     ...form.getHeaders(),
//   },
// })
//   .then(response => {
//     console.log('Success:', response.data);
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });

async function send(){
  try{
    const response=await axios.post('http://127.0.0.1:8000/createcomment/',{token:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5ODM4MTI0LCJpYXQiOjE3Mjk0MjgwNzgsImp0aSI6ImQyZjBhYWQ2NDgwZTQ5MGE4MmNjNjRiNzk1Y2Q4ZmFmIiwidXNlcl9pZCI6N30.DF3bbR7uigqny5tGVK0A9KxW-ftC-j-DcS7DvuSVGVk",id:"1a48b534-56f3-4f7d-9619-fc2831047518",comment:"scommentonit"})
    console.log(response.status,"comes",response.data)
  }
  catch(error) {
    console.log(error,"issues")
  }
  
}

send()
