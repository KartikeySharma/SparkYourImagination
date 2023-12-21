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
    book_details = df[df['title_A'] == selected_title]
    # st.write(book_details)
    min_dist_book = book_details[book_details['distCol'] == book_details['distCol'].min()]

    if st.button("Get Books"):
        if not min_dist_book.empty:
            min_dist_book = min_dist_book.iloc[0]  # Select the first row from the filtered DataFrame
            st.write(f"Book similar to {min_dist_book['title_A']}:")
            st.write("")
            st.write("")
            
            # Display books' images with book names in a horizontal grid
            image_html = get_image(min_dist_book['image_url_B'], 200)
            if image_html:
                st.markdown(f'<div style="display: flex; flex-direction: column; align-items: center; text-align: center;"> \
                        <img src="data:image/jpeg;base64,{image_html}" style="width:200px; margin: 0 10px"> \
                        <div style="font-size: 0.8em; word-wrap: break-word;">{min_dist_book["title_B"]}</div> \
                        </div>', unsafe_allow_html=True)
        else:
            st.write(f"No books found for {selected_title}.")


# Create Streamlit app

# CSS for sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the sidebar width
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        width: 250px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set page width
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Spark Your Imagination !",
    ("Book Recommender (Collaborative)", "Content-based Recommender")
)

if page == "Book Recommender (Collaborative)":
    st.title('Spark Your Imagination')
    getTop5Books()

elif page == "Content-based Recommender":
    st.title("Content-based Recommender")
    getClosestBook()
