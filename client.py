import requests

# The URL to which you want to send the request
url = 'http://127.0.0.1:8000/save/'  # Replace with your actual endpoint

# Open the image file in binary mode
image_path = r"C:\Users\Pritimaya Sahoo\OneDrive\Pictures\IMG-20221216-WA0005.jpg"  
# Provide the correct path to your image
with open(image_path, 'rb') as img_file:
    # Prepare form data with the token and image
    files = {
        'image': img_file  # The key should match what the Django view is expecting
    }
    
    # You can send token and other data as part of the form
    data = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5Nzg1NjI1LCJpYXQiOjE3Mjk0MjgwNzgsImp0aSI6IjdlZjdkZTBjZTAwMTRiNDk5Yzc0OWIwMzU3ODNmZGFkIiwidXNlcl9pZCI6N30.MH7bznm2ZlUHxFGF7LgV6YXr32l6wunxwa6KZ8MTnIY'  # Replace with your actual token
    }

    # Send the POST request
    response = requests.post(url, files=files, data=data)

    # Print response from the server
    print(response.status_code)
    print(response.json())
