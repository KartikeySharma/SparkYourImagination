import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
import base64

def load_data(str):
    # Load your CSV file here
    df = pd.read_csv(str)
    return df

def getTop5Books():

    # data_load_state = st.text('Loading CSV data...')
    df = load_data('output_final.csv')
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


def getClosestBook():
    df = load_data('content.csv')
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
        
    selected_title = st.selectbox("Select a Title", df['title_A'].unique())

    # Display details of the selected book
    min_dist_book = df[df['title_A'] == selected_title]
    # st.write(book_details)
    # min_dist_book = book_details[book_details['distCol'] == book_details['distCol'].min()]

    if st.button("Get Books"):
        books_with_images = min_dist_book  # Assuming min_dist_book is the DataFrame with book data
        if not books_with_images.empty:
            st.write(f"Books similar to {min_dist_book.iloc[0]['title_A']}:")
            st.write("")
            st.write("")
            
            # Display books' images with book names in a horizontal grid
            image_width = 200  # Set the width of each image
            images_html = ""
            for index, row in books_with_images.iterrows():
                image_html = get_image(row['image_url_B'], image_width)  # Assuming 'image_url_B' contains image URLs
                if image_html:
                    images_html += f'<div style="display: inline-block; text-align: center;">'
                    images_html += f'<img src="data:image/jpeg;base64,{image_html}" style="width:{image_width}px; margin: 0 10px">'
                    images_html += f'<div style="font-size: 0.8em; word-wrap: break-word; width: {image_width}px;">{row["title_B"]}</div>'
                    images_html += f'</div>'
            
            # Display images in a horizontal grid
            st.markdown(images_html, unsafe_allow_html=True)
        else:
            st.write(f"No books found for {selected_title}.")


import streamlit as st

# CSS for sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the sidebar width and style
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 250px;
    }
    .sidebar .sidebar-content .block-container {
        padding: 20px;
    }
    .sidebar .sidebar-content .block-container hr {
        margin-top: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set page width and padding
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 20px;
        padding-left: 30px;
        padding-right: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with navigation options
page = st.sidebar.radio(
    "Navigation",
    ("Home", "Book Recommender (Collaborative)", "Content-based Recommender")
)

# Main content based on selected page
if page == "Home":
    local_image_path = 'logo.png'

    # Read the image file as bytes
    with open(local_image_path, 'rb') as f:
        image_bytes = f.read()

    # Encode the image as base64
    encoded_image = base64.b64encode(image_bytes).decode()

    # Center the image and text using HTML/CSS
    centered_content_html = f"""
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
            <img src="data:image/png;base64,{encoded_image}" style="width: 400px; height: 400px;">
            <h5 style="margin-top: 20px;">Choose an option from the sidebar to get started.</h5>
        </div>
    """

    # Display the centered content using Markdown
    st.markdown(centered_content_html, unsafe_allow_html=True)

elif page == "Book Recommender (Collaborative)":
    st.title('Collaborative Filtering Recommender')
    getTop5Books()  # Function for displaying collaborative recommendations
elif page == "Content-based Recommender":
    st.title("Content-based Recommender")
    getClosestBook()  # Function for content-based recommendations
