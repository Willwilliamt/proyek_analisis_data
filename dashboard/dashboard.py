import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

# Load datasets
order_items = pd.read_csv('data/order_items_dataset.csv')
order_payments = pd.read_csv('data/order_payments_dataset.csv')
order_reviews = pd.read_csv('data/order_reviews_dataset.csv')
orders = pd.read_csv('data/orders_dataset.csv')
products = pd.read_csv('data/products_dataset.csv')
product_category_translation = pd.read_csv('data/product_category_name_translation.csv')
sellers = pd.read_csv('data/sellers_dataset.csv')
customers = pd.read_csv('data/customers_dataset.csv')
geolocation = pd.read_csv('data/geolocation_dataset.csv')
st.sidebar.title("Filters")

start_date = st.sidebar.date_input('Start date', pd.to_datetime('2016-02-02'))
end_date = st.sidebar.date_input('End date', pd.to_datetime('2018-01-01'))
selection = st.sidebar.radio(
    "Pilih", 
    ("Visualisasi", "Explore Data Analysis", "Pertanyaan 1","Pertanyaan 2","RFM")
)   
filtered_orders = orders[(orders['order_purchase_timestamp'] >= str(start_date)) & 
                          (orders['order_purchase_timestamp'] <= str(end_date))]

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
filtered_orders = orders[(orders['order_purchase_timestamp'] >= str(start_date)) & 
                          (orders['order_purchase_timestamp'] <= str(end_date))]

if selection == "Visualisasi":
    st.title("E-Commerce Dashboard")
    st.subheader("Sales Overview")
    sales_data = filtered_orders.groupby('order_purchase_timestamp').size().reset_index(name='order_count')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=sales_data, x='order_purchase_timestamp', y='order_count', ax=ax)
    ax.set_title('Sales Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Orders')
    st.pyplot(fig)
    product_sales = filtered_orders.merge(order_items, on='order_id')
    product_sales = product_sales.merge(products, on='product_id')
    product_sales = product_sales.merge(product_category_translation, on='product_category_name')
    product_category_sales = product_sales.groupby('product_category_name').size().reset_index(name='order_count')
    top_n_categories = product_category_sales.sort_values(by='order_count', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=top_n_categories, x='product_category_name', y='order_count', ax=ax)
    ax.set_title("Sales by Product Category")
    ax.set_xlabel('Product Category')
    ax.set_ylabel('Number of Orders')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")


    st.pyplot(fig)

    payment_sales = order_payments.merge(filtered_orders, on='order_id')
    payment_sales = payment_sales.groupby('payment_type').size().reset_index(name='order_count')

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=payment_sales, x='payment_type', y='order_count', ax=ax)
    ax.set_title("Payment Methods Distribution")
    ax.set_xlabel('Payment Type')
    ax.set_ylabel('Number of Orders')
    st.pyplot(fig)
elif selection == "Pertanyaan 1":
    st.title("Pertanyaan 1 Dashboard")
    #pertanyaan 1
    order_items_products = pd.merge(order_items, products, on='product_id')
    order_items_products = pd.merge(order_items_products, product_category_translation, on='product_category_name', how='left')
    payment_orders = pd.merge(order_payments, orders, on='order_id', how='left')
    payment_customer = pd.merge(payment_orders, customers, on='customer_id', how='left')
    payment_by_state = payment_customer.groupby(['customer_state', 'payment_type']).size().reset_index(name='payment_count')
    top_payment_by_state = payment_by_state.loc[payment_by_state.groupby('customer_state')['payment_count'].idxmax()]
    print(top_payment_by_state.head(10))
    st.title('Analisis Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah')
    st.dataframe(top_payment_by_state.head(10))
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='payment_count', y='customer_state', hue='payment_type', data=top_payment_by_state, palette='viridis', ax=ax)
    ax.set_title('Metode Pembayaran Paling Sering Digunakan Berdasarkan Wilayah')
    ax.set_xlabel('Jumlah Pembayaran')
    ax.set_ylabel('Wilayah')
    st.pyplot(fig)


elif selection == "Pertanyaan 2":
    st.title("Pertanyaan 2 Dashboard")
    order_items_products = pd.merge(order_items, products, on='product_id')
    order_items_products = pd.merge(order_items_products, product_category_translation, on='product_category_name', how='left')
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
    st.title('Analisis Pembelian Terbanyak Berdasarkan Kategori Produk')
    st.dataframe(category_sales.head(10))

    plt.figure(figsize=(10,6))
    sns.barplot(x='order_count', y='product_category', data=category_sales.head(10), palette='viridis')
    plt.title('10 Kategori Produk dengan Pesanan Terbanyak')
    st.pyplot(plt)
elif selection == "Explore Data Analysis":
    st.title("Explore Data Analysis Dashboard")
    st.header('Jumlah Pesanan Per Bulan')
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_month'] = orders['order_purchase_timestamp'].dt.month
    orders['order_year'] = orders['order_purchase_timestamp'].dt.year

    orders_monthly = orders.groupby('order_month')['order_id'].count()
    plt.figure(figsize=(10, 6))
    orders_monthly.plot(kind='line', title="Jumlah Pesanan Per Bulan")
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Pesanan')
    st.pyplot(plt)
    st.header('Produk Yang Paling Sering Dipesan')
    order_items_count = order_items['product_id'].value_counts()
    st.subheader('Most Ordered Products (Top 10)')
    st.dataframe(order_items_count.head(10))
    plt.figure(figsize=(12, 6))
    order_items_count.head(10).plot(kind='bar', title="Top 10 Produk yang Paling Sering Dipesan")
    plt.xlabel('Product ID')
    plt.ylabel('Jumlah Pemesanan')
    st.pyplot(plt)
    st.header('Jenis Pembayaran dan Jumlahnya')
    payment_type_count = order_payments['payment_type'].value_counts()
    st.dataframe(payment_type_count)
    plt.figure(figsize=(10, 6))
    payment_type_count.plot(kind='bar', title="Jenis Pembayaran dan Jumlahnya")
    plt.xlabel('Jenis Pembayaran')
    plt.ylabel('Jumlah Pembayaran')
    st.pyplot(plt)
    
    st.header("Review Score Dari Pelanggan")
    review_rating_count = order_reviews['review_score'].value_counts()
    print("Review Score Distribution:\n", review_rating_count)
    st.dataframe(review_rating_count)
    plt.figure(figsize=(10, 6))
    review_rating_count.sort_index().plot(kind='bar', title="Review Score")
    plt.xlabel('Skor Ulasan')
    plt.ylabel('Jumlah Ulasan')
    st.pyplot(plt)
    
    st.header("Top 10 Kategori Produk")
    product_category_count = products['product_category_name'].value_counts()
    print("Top 10 Kategori Produk:\n", product_category_count)

    plt.figure(figsize=(12, 8))
    product_category_count.head(10).plot(kind='bar', title="Top 10 Kategori Produk")
    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Produk')
    st.pyplot(plt)
    
    st.header("Top 10 Kota dengan Lokasi Pelanggan Terbanyak")
    geolocation_location_count = geolocation['geolocation_city'].value_counts()
    print("Top 10 Kota dengan Lokasi Pelanggan Terbanyak:\n", geolocation_location_count)

    plt.figure(figsize=(12, 6))
    geolocation_location_count.head(10).plot(kind='bar', title="Top 10 Kota dengan Lokasi Pelanggan Terbanyak")
    plt.xlabel('Kota')
    plt.ylabel('Jumlah Pelanggan')
    st.pyplot(plt)
elif selection == "RFM":
    st.title("RFM Dashboard")
    merged_data = pd.merge(orders, order_items, on='order_id')
    latest_date = pd.to_datetime(merged_data['order_purchase_timestamp']).max()
    merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])
    rfm_data = merged_data.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,
        'order_id': 'count', 
        'price': 'sum' 
    }).reset_index()

    rfm_data.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

    st.title('RFM Analysis (Recency, Frequency, Monetary)')
    st.subheader('RFM Data')
    st.subheader('Analisis RFM bertujuan untuk menemukan 3 aspek')
    st.write("""
    - **Recency**: Mengukur berapa lama pelanggan terakhir kali melakukan pembelian.
    - **Frequency**: Menghitung seberapa sering pelanggan melakukan pembelian.
    - **Monetary**: Mengukur seberapa banyak pelanggan membelanjakan uang mereka.
    """)
    st.dataframe(rfm_data.head()) 

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=rfm_data, x='Recency', y='Frequency', size='Monetary', sizes=(20, 200), ax=ax, legend=False)
    ax.set_title('RFM Analysis')
    ax.set_xlabel('Recency (days since last purchase)')
    ax.set_ylabel('Frequency (number of purchases)')
    st.pyplot(fig)
    plt.show()

