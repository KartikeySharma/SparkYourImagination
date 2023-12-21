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

# def get_image(image_url):
#     try:
#         response = requests.get(image_url)
#         img = Image.open(BytesIO(response.content))
#         buffered = BytesIO()
#         img.save(buffered, format="JPEG")
#         img_str = base64.b64encode(buffered.getvalue()).decode()
#         return f'<img src="data:image/jpeg;base64,{img_str}" alt="book_image">'
#     except Exception as e:
#         st.error(f"Error fetching image: {e}")
#         return None

def get_resized_image(image_url, target_size):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail(target_size, Image.ANTIALIAS)
        return img
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return None
    
# Display dropdown for selecting user ID
selected_user_id = st.selectbox("Select a User ID", user_ids) 

if st.button("Get Books"):
    filtered_books = books_df[books_df['original_user_id'] == selected_user_id][['book_id', 'book_name', 'image_url']]
    books_with_images = filtered_books.copy()
    if not filtered_books.empty:
        st.write(f"Books for User ID {selected_user_id}:")
        target_image_size = (200, 200)  # Adjust width and height here
        books_with_images['image'] = books_with_images['image_url'].apply(lambda x: get_resized_image(x, target_image_size))
        books_with_images = books_with_images[['book_name', 'image']]

        for index, row in books_with_images.iterrows():
            if row['image'] is not None:
                st.image(row['image'], caption=row['book_name'], use_column_width=True)
    else:
        st.write(f"No books found for User ID {selected_user_id}.")