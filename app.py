import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Dummy book data (replace this with your actual data)
book_data = {
    "book_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    "original_user_id": ["1","1","1","2","2","2","3","3","3","4","4","4","5","5","5"],
    "book_id": ["1","2","3","4","5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    "book_name": ["b1","b2","b3","b4","b5", "b6","b7","b8","b9", "b10","b11","b12","b13","b14","b15"],
    "image_url": 
        [
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
        "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg"
        ]
}

books_df = pd.DataFrame(book_data)

# Get unique user IDs
user_ids = books_df['original_user_id'].unique().tolist()

# Create Streamlit app
st.title('Books for User ID')

def get_image(image_url, image_width=200):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((image_width, image_width))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f'{img_str}'
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return None

# Create a copy of the DataFrame to store the images

# Display dropdown for selecting user ID
selected_user_id = st.selectbox("Select a User ID", user_ids) 

if st.button("Get Books"):
    st.write(f"Books for User ID {selected_user_id}:")
    books_with_images = books_df[books_df['original_user_id'] == selected_user_id][['book_id', 'book_name', 'image_url']]
    if not books_with_images.empty:
        st.write(f"Books for User ID {selected_user_id}:")
        
        # Display books' images in a horizontal grid
        image_width = 200  # Set the width of each image
        images_html = ""
        for index, row in books_with_images.iterrows():
            image_html = get_image(row['image_url'], image_width)
            if image_html:
                images_html += f'<img src="data:image/jpeg;base64,{image_html}" style="width:{image_width}px; margin: 0 10px">'

        # Display images in a horizontal grid
        st.markdown(images_html, unsafe_allow_html=True)
    else:
        st.write(f"No books found for User ID {selected_user_id}.")