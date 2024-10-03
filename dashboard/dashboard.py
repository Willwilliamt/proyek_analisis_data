import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# Load datasets
order_items = pd.read_csv('sampledata/order_items_dataset.csv')
order_payments = pd.read_csv('sampledata/order_payments_dataset.csv')
order_reviews = pd.read_csv('sampledata/order_reviews_dataset.csv')
orders = pd.read_csv('sampledata/orders_dataset.csv')
products = pd.read_csv('sampledata/products_dataset.csv')
product_translation = pd.read_csv('sampledata/product_category_name_translation.csv')
sellers = pd.read_csv('sampledata/sellers_dataset.csv')
customers = pd.read_csv('sampledata/customers_dataset.csv')
geolocation = pd.read_csv('sampledata/geolocation_dataset.csv')


# Streamlit UI Layout
st.title("E-Commerce Dashboard")
st.sidebar.title("Filters")

# Date range for sales visualization
start_date = st.sidebar.date_input('Start date', pd.to_datetime('2016-02-02'))
end_date = st.sidebar.date_input('End date', pd.to_datetime('2018-01-01'))
selection = st.sidebar.radio(
    "Tunjukaan Jawaban Pertanyaan", 
    ("Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah", "Kategori Produk dengan Pesanan Terbanyak")
)
# Filter orders by date
filtered_orders = orders[(orders['order_purchase_timestamp'] >= str(start_date)) & 
                          (orders['order_purchase_timestamp'] <= str(end_date))]

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
filtered_orders = orders[(orders['order_purchase_timestamp'] >= str(start_date)) & 
                          (orders['order_purchase_timestamp'] <= str(end_date))]

# Display sales data
st.subheader("Sales Overview")

# Total sales value over time
sales_data = filtered_orders.groupby('order_purchase_timestamp').size().reset_index(name='order_count')

# Plot sales over time
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=sales_data, x='order_purchase_timestamp', y='order_count', ax=ax)
ax.set_title('Sales Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Number of Orders')
st.pyplot(fig)

# Product category sales
product_sales = filtered_orders.merge(order_items, on='order_id')
product_sales = product_sales.merge(products, on='product_id')
product_sales = product_sales.merge(product_translation, on='product_category_name')

# Group by product category
product_category_sales = product_sales.groupby('product_category_name').size().reset_index(name='order_count')

# Sort by order count and take the top N categories to avoid overcrowding
top_n_categories = product_category_sales.sort_values(by='order_count', ascending=False).head(10)

# Plot product category sales
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_n_categories, x='product_category_name', y='order_count', ax=ax)

# Set the title and labels
ax.set_title("Sales by Product Category")
ax.set_xlabel('Product Category')
ax.set_ylabel('Number of Orders')

# Rotate the x-axis labels for better readability
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

# Optionally, if category names are still too long, you can abbreviate them:
# top_n_categories['product_category_name'] = top_n_categories['product_category_name'].str.slice(0, 20)

st.pyplot(fig)

# Payment methods distribution
payment_sales = order_payments.merge(filtered_orders, on='order_id')
payment_sales = payment_sales.groupby('payment_type').size().reset_index(name='order_count')

# Plot payment method distribution
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=payment_sales, x='payment_type', y='order_count', ax=ax)
ax.set_title("Payment Methods Distribution")
ax.set_xlabel('Payment Type')
ax.set_ylabel('Number of Orders')
st.pyplot(fig)
order_items_products = pd.merge(order_items, products, on='product_id')
order_items_products = pd.merge(order_items_products, product_translation, on='product_category_name', how='left')
payment_orders = pd.merge(order_payments, orders, on='order_id', how='left')
# Gabungkan data yang sudah digabungkan dengan data customers untuk mendapatkan informasi wilayah (customer_city atau customer_state)
payment_customer = pd.merge(payment_orders, customers, on='customer_id', how='left')

# Hitung jumlah penggunaan metode pembayaran berdasarkan wilayah (contoh menggunakan customer_state)
payment_by_state = payment_customer.groupby(['customer_state', 'payment_type']).size().reset_index(name='payment_count')

# Pilih metode pembayaran yang paling sering digunakan untuk setiap wilayah
top_payment_by_state = payment_by_state.loc[payment_by_state.groupby('customer_state')['payment_count'].idxmax()]

if selection == "Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah":
    # Menampilkan data
    print(top_payment_by_state.head(10))

    # Plot visualisasi
    st.title('Analisis Metode Pembayaran Berdasarkan Wilayah')

    st.header('Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah')
    st.dataframe(top_payment_by_state.head(10))

    # Visualisasi menggunakan barplot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='payment_count', y='customer_state', hue='payment_type', data=top_payment_by_state, palette='viridis', ax=ax)
    ax.set_title('Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah')
    ax.set_xlabel('Jumlah Pembayaran')
    ax.set_ylabel('Wilayah')

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

elif selection == "Kategori Produk dengan Pesanan Terbanyak":
    order_items_products = pd.merge(order_items, products, on='product_id')
    order_items_products = pd.merge(order_items_products, product_translation, on='product_category_name', how='left')
    print(order_items_products.head())
    category_sales = order_items_products['product_category_name_english'].value_counts().reset_index()
    category_sales.columns = ['product_category', 'order_count']
    print(category_sales.head(10))
    plt.figure(figsize=(10,6))
    sns.barplot(x='order_count', y='product_category', data=category_sales.head(10), palette='viridis')
    plt.title('10 Kategori Produk dengan Pesanan Terbanyak')
    plt.xlabel('Jumlah Pesanan')
    plt.ylabel('Kategori Produk')
    plt.show()
    st.title('Analisis Pola Pembelian Berdasarkan Kategori Produk')
    st.header('Pola Pembelian Berdasarkan Kategori Produk')
    st.dataframe(category_sales.head(10))

    plt.figure(figsize=(10,6))
    sns.barplot(x='order_count', y='product_category', data=category_sales.head(10), palette='viridis')
    plt.title('10 Kategori Produk dengan Pesanan Terbanyak')
    st.pyplot(plt)



