import streamlit as st
import pandas as pd
import joblib
import time

# Load the model and scaler
model = joblib.load('restaurant_rating_predictor.pkl')
scaler = joblib.load('scaler.pkl')

# Add custom CSS for door opening effect and background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('background_image_url'); /* Replace with your image URL */
        background-size: cover;
        background-position: center;
    }
    .stTitle {
        font-size: 36px;
        color: #4CAF50;
        text-align: center;
        padding: 20px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 8px;
    }
    /* Door animation */
    .door-container {
        position: relative;
        width: 200px;
        height: 300px;
        margin: auto;
        display: none; /* Initially hide the door */
    }
    .door {
        position: absolute;
        width: 100%;
        height: 100%;
        background: #6B8E23;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        transform-origin: left;
        transition: transform 1s ease-in-out;
    }
    .door.open {
        transform: rotateY(-120deg);
    }
    .door::before {
        content: '';
        position: absolute;
        width: 50%;
        height: 100%;
        background: #4CAF50;
        left: 0;
        border-right: 2px solid #4CAF50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the door HTML
st.markdown(
    """
    <div class="door-container" id="doorContainer">
        <div class="door" id="door"></div>
    </div>
    <script>
    function openDoor() {
        document.getElementById('doorContainer').style.display = 'block'; // Show the door container
        document.getElementById('door').classList.add('open');
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Set up the Streamlit app
st.title('Restaurant Rating Prediction')

# Display the restaurant image
st.image('restaurant.jpeg', use_column_width=True)

# Sidebar setup
st.sidebar.header('Restaurant Rating Prediction Settings')

# User inputs in sidebar
restaurant_name = st.sidebar.text_input('Restaurant Name:')
city = st.sidebar.text_input('City:')
address = st.sidebar.text_input('Address:')
locality = st.sidebar.text_input('Locality:')
locality_verbose = st.sidebar.text_input('Locality Verbose:')
cuisines = st.sidebar.text_input('Cuisines:')
currency = st.sidebar.text_input('Currency:')
has_table_booking = st.sidebar.selectbox('Has Table Booking?', [0, 1])
has_online_delivery = st.sidebar.selectbox('Has Online Delivery?', [0, 1])
is_delivering_now = st.sidebar.selectbox('Is Delivering Now?', [0, 1])
switch_to_order_menu = st.sidebar.selectbox('Switch to Order Menu?', [0, 1])
rating_color = st.sidebar.selectbox('Rating Color:', ['Dark Green', 'Green', 'Yellow', 'Orange', 'White', 'Red'])
rating_text = st.sidebar.selectbox('Rating Text:', ['Excellent', 'Very Good', 'Good', 'Average', 'Not rated', 'Poor'])
average_cost = st.sidebar.slider('Average Cost for Two', 0, 1000, 100)
price_range = st.sidebar.slider('Price Range', 1, 4, 2)
votes = st.sidebar.slider('Votes', min_value=0, max_value=11000, step=50)

# Main content
st.markdown('<h1 class="stTitle">Restaurant Rating Prediction</h1>', unsafe_allow_html=True)

# Convert user inputs to DataFrame
user_data = pd.DataFrame({
    'Restaurant Name': [restaurant_name],
    'City': [city],
    'Address': [address],
    'Locality': [locality],
    'Locality Verbose': [locality_verbose],
    'Cuisines': [cuisines],
    'Currency': [currency],
    'Has Table booking': [has_table_booking],
    'Has Online delivery': [has_online_delivery],
    'Is delivering now': [is_delivering_now],
    'Switch to order menu': [switch_to_order_menu],
    'Rating color': [rating_color],
    'Rating text': [rating_text],
    'Average Cost for two': [average_cost],
    'Price range': [price_range],
    'Votes': [votes]
})

# Add a "Predict" button
if st.button('Predict'):
    with st.spinner('Calculating...'):
        time.sleep(2)
        prediction = model.predict(user_data)
        st.success(f"Predicted Rating: {prediction[0]:.2f}")
        
        # Trigger the door opening animation
        st.markdown(
            """
            <script>
            openDoor();
            </script>
            """,
            unsafe_allow_html=True
        )
