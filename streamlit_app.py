import streamlit as st
import requests
import json

API_URL = "http://localhost:8080"


def fetch_products():
    response = requests.get(f"{API_URL}/products")
    return response.json()


def create_product(name, price):
    data = {"name": name, "price": price}
    response = requests.post(f"{API_URL}/products", json=data)
    return response.json()


def get_product(id):
    response = requests.get(f"{API_URL}/products/{id}")
    return response.json()


def update_product(id, name, price):
    data = {"name": name, "price": price}
    response = requests.put(f"{API_URL}/products/{id}", json=data)
    return response.json()


def delete_product(id):
    response = requests.delete(f"{API_URL}/products/{id}")
    return response.json()


st.title("FastAPI CRUD MongoDB Demo")

# Fetch and display all products
st.header("All Products")
products = fetch_products()
for product in products:
    st.write(
        f"ID: {product['id']}, Name: {product['name']}, Price: ${product['price']}"
    )

# Create a new product
st.header("Create New Product")
new_name = st.text_input("Product Name")
new_price = st.number_input("Product Price", min_value=0, step=1)
if st.button("Create Product"):
    result = create_product(new_name, new_price)
    st.success(f"Product created: {result}")

# Get a product
st.header("Get Product")
get_id = st.text_input("Product ID to Get")
if st.button("Get Product"):
    result = get_product(get_id)
    st.success(f"Product: {result}")


# Update a product
st.header("Update Product")
update_id = st.text_input("Product ID to Update")
update_name = st.text_input("New Product Name")
update_price = st.number_input("New Product Price", min_value=0, step=1)
if st.button("Update Product"):
    result = update_product(update_id, update_name, update_price)
    st.success(f"Product updated: {result}")


# Delete a product
st.header("Delete Product")
delete_id = st.text_input("Product ID to Delete")
if st.button("Delete Product"):
    result = delete_product(delete_id)
    st.success(f"Product deleted: {result}")


st.info(
    "Note: This Streamlit app assumes that the FastAPI backend is running on http://localhost:8080. Make sure to start the FastAPI server before using this interface."
)
