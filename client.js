const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');

const Cookies = require('universal-cookie');

const cookies = new Cookies();

const csrftoken = cookies.get('csrftoken');

axios.defaults.withCredentials = true;

axios.defaults.credentials = 'same-origin';

axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

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
    const response=await axios.post('http://127.0.0.1:8000/follow/',{token:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMDA2ODc3LCJpYXQiOjE3Mjk4NDUzMTYsImp0aSI6ImUzZTFiMzYxN2NiZTQ0YzU5YTE0Y2VkMWUwOWI0NjIwIiwidXNlcl9pZCI6N30.BIehlSL5i1zxrinuIhWhjNepuYdR7nXYqfB8wW2tBhQ",another_id:"8"})
    console.log(response.status,"comes",response.data)
  }
  catch(error) {
    console.log(error,"issues")
  }
  
}


//send()


async function uploadImage() {
  try {
    // Prepare the form data
    const form = new FormData();
    form.append('token', 'your_token_here'); // Add token to form
    form.append('image', fs.createReadStream('path/to/your/image.jpg')); // Path to your image

    // Send the request
    const response = await axios.post('http://127.0.0.1:8000/upload-image', form, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('Success:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
}

// Call the function
//uploadImage();

async function profileget(){
  try{
    const response=await axios.get('http://127.0.0.1:8000/profile/',{ params: {token:"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5OTI4NTIxLCJpYXQiOjE3Mjk4NDUzMTYsImp0aSI6ImY5YWRlNTBiOGRmYzRhZDJhMDgxZjc1MzM1MWExMjg4IiwidXNlcl9pZCI6N30.eouVyBvc-B08FxG0sB0Uqd_2Kl_JlxG1mUYUV_kySco"}})
    console.log(response.status,"comes",response.data)
  }
  catch(error) {
    console.log(error,"issues")
  }
  
}

//profileget()



async function profilepost() {
  try {
    // Prepare the form data
    const form = new FormData();
    form.append('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5OTI4NTIxLCJpYXQiOjE3Mjk4NDUzMTYsImp0aSI6ImY5YWRlNTBiOGRmYzRhZDJhMDgxZjc1MzM1MWExMjg4IiwidXNlcl9pZCI6N30.eouVyBvc-B08FxG0sB0Uqd_2Kl_JlxG1mUYUV_kySco'); // Add token to form
    form.append('profile_image', fs.createReadStream("C://Users//Pritimaya Sahoo//OneDrive//Pictures//kohil.jpg")); // Path to your image
    form.append('name',"chiku sahoo")
    form.append('about',"i am a student")
    form.append('school',"ssvm")

    // Send the request
    const response = await axios.post('http://127.0.0.1:8000/profile/', form, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    console.log('Success:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
}

//profilepost()
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

async function fetchCSRFToken() {
  try {
      const response = await axios.get('http://127.0.0.1:8000/get-csrf-token/');
      console.log(response.data.csrfToken,"token come")
      //axios.defaults.headers.common['X-CSRFToken'] = response.data.csrfToken;
      const responsecome = await axios.post(
        'http://127.0.0.1:8000/follow/',
        {
          token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMDA2ODc3LCJpYXQiOjE3Mjk4NDUzMTYsImp0aSI6ImUzZTFiMzYxN2NiZTQ0YzU5YTE0Y2VkMWUwOWI0NjIwIiwidXNlcl9pZCI6N30.BIehlSL5i1zxrinuIhWhjNepuYdR7nXYqfB8wW2tBhQ",
          another_id: "8",
        },
        {
          headers: {
            'X-CSRFToken': response.data.csrfToken,  // Set the CSRF token manually in the header
          },
          withCredentials: true,  // Ensure cookies are sent with the request
        }
      );
      console.log(responsecome.status,"comes",response.data)
  } catch (error) {
      console.error('Failed to fetch CSRF token:', error);
  }
}

// Call this function once when your app initializes
fetchCSRFToken();
