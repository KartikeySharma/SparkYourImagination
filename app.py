import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

# Dummy book data (replace this with your actual data)
# book_data = {
#     "book_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
#     "original_user_id": ["1","1","1","2","2","2","3","3","3","4","4","4","5","5","5"],
#     "book_id": ["1","2","3","4","5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
#     "book_name": ["b1","b2","b3","b4","b5", "b6","b7","b8","b9", "b10","b11","b12","b13","b14","b15"],
#     "image_url": 
#         [
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg",
#         "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1417983381i/23316548.jpg"
#         ]
# }

# books_df = pd.DataFrame(book_data)

def load_data():
    # Load your CSV file here
    # Replace 'path_to_your_csv_file' with the path to your CSV file
    df = pd.read_csv('out.csv')
    return df

# Get unique user IDs
# user_ids = books_df['original_user_id'].unique().tolist()

# Create Streamlit app
st.title('Books for User ID')

# data_load_state = st.text('Loading CSV data...')
df = load_data()
# data_load_state.text('Loading CSV data... done!')
placeholder_url = "https://img.freepik.com/premium-vector/book-design-icon-flat-illustration-book-design-vector-icon-isolated-white-background_98396-6329.jpg"

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
        response = requests.get(placeholder_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((image_width, image_width))
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f'{img_str}'
        # st.error(f"Error fetching image: {e}")
        # return None

# Create a copy of the DataFrame to store the images

# Display dropdown for selecting user ID
user_ids = df['original_user_id'].unique()
selected_user_id = st.selectbox("Select a User ID", user_ids) 

if st.button("Get Books"):
    books_with_images = df[df['original_user_id'] == selected_user_id][['book_id', 'book_name', 'image_url']]
    if not books_with_images.empty:
        st.write(f"Books for User ID {selected_user_id}:")
        st.write("")
        st.write("")
        
        # Display books' images with book names in a horizontal grid
        image_width = 200  # Set the width of each image
        images_html = ""
        count = 0
        for index, row in books_with_images.iterrows():
            image_html = get_image(row['image_url'], image_width)
            if image_html:
                images_html += f'<div style="display: inline-block; text-align: center;">'
                images_html += f'<img src="data:image/jpeg;base64,{image_html}" style="width:{image_width}px; margin: 0 10px">'
                images_html += f'<div style="font-size: 0.8em; word-wrap: break-word; width: {image_width}px;">{row["book_name"]}</div>'
                images_html += f'</div>'
                count += 1
                if count % 3 == 0:
                    images_html += '<br> <br>'  # Start a new line after every 3 books
        
        # Display images in a horizontal grid with maximum 3 books per row
        st.markdown(images_html, unsafe_allow_html=True)
    else:
        st.write(f"No books found for User ID {selected_user_id}.")
