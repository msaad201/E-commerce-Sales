# Amazon Products Sales Data: Cleaning & Feature Engineering

A mid-project that takes a raw, messy Amazon product listings dataset (`amazon_products_sales_data_uncleaned.csv`) and turns it into a clean, analysis-ready table.

**Tools used:** Python, pandas, NumPy, scikit-learn (`KNNImputer`), Jupyter Notebook (VS Code)

## Get started

### Requirements

- Python 3.10 or newer
- VS Code with the Python and Jupyter extensions to run the notebook
- The raw CSV file `amazon_products_sales_data_uncleaned.csv` in the project
  folder (included in this repository)

The `requirements.txt` file contains the packages used by both the notebook and
the dashboard.

### Install dependencies

From the project folder, create a virtual environment and install the
dependencies in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Run the data-cleaning notebook

Open `Mid_project_amazon_sales.ipynb` in VS Code, select the `.venv` Python
environment as the notebook kernel, and run the cells from top to bottom. The
notebook reads `amazon_products_sales_data_uncleaned.csv` and writes
`Mid_project_amazon_sales_cleaned.parquet` to the project folder. The cleaned
Parquet file is already included, so you can skip this step if you do not need
to regenerate it.

### Run the Streamlit dashboard

From the project folder, run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run home_page.py
```

Streamlit opens the dashboard in your browser. It includes Overview, Pricing
and Discounts, Delivery, Ratings and Reviews, and Data Explorer pages. Shared
date, delivery, sponsored-status, and availability filters are in the sidebar.
The `Revenue_last_month` field is an approximate monthly sales-volume estimate,
not revenue in dollars.

Streamlit is configured to use dark mode by default for every visitor. The
shared theme keeps the dashboard dark regardless of the visitor's operating
system appearance preference.

---

## 1. Original Columns and Their Meaning

| Original column | What it means |
|---|---|
| `title` | Product name and description as shown on Amazon. |
| `rating` | Average customer star rating, out of 5. |
| `number_of_reviews` | How many customers reviewed the product. |
| `bought_in_last_month` | Approximate number of units bought in the past month, written as text such as "100+" or "2K+". |
| `current/discounted_price` | The price the customer pays right now. |
| `price_on_variant` | Price of the default variant (size, pack, color, etc.). |
| `listed_price` | Original price before any discount, or "No Discount" if there is none. |
| `is_best_seller` | Product badge such as "Best Seller", "Amazon's Choice" or "Limited time deal". "No Badge" means none. |
| `is_sponsored` | Whether the product is a paid ad ("Sponsored") or a normal result ("Organic"). |
| `is_couponed` | Whether a coupon is available and how much it saves, e.g. "Save 15% with coupon". |
| `buy_box_availability` | Whether the product has an "Add to cart" button. Empty means it can't be bought directly. |
| `delivery_details` | Estimated delivery date and shipping info shown on the listing. |
| `sustainability_badges` | Extra labels such as "Small Business" or "Works with Alexa". Mostly empty. |
| `image_url` | Link to the product picture. |
| `product_url` | Link to the product page on Amazon. |
| `collected_at` | Date and time the data was scraped. |

---

## 2. Column Name Changes (Old → New)

| Old name | New name | Notes |
|---|---|---|
| `title` | `Product_Name` | Clearer name. |
| `collected_at` | `Order_Placed` | Converted to datetime. It is the date the listing was collected, and it is used as the reference date for delivery time. |
| `bought_in_last_month` | `Revenue_last_month` | Converted to a number. It holds the approximate monthly sales volume taken from the "bought in last month" label, not a money amount. |
| `current/discounted_price` | `Price_after_Discount` | Converted to a number. |
| `buy_box_availability` | `is_available` | Values changed to "Available" / "Not Available". |
| `is_best_seller` | `Best_seller` | Replaced by a simplified column (see section 4), then dropped. |
| `delivery_details` | `delivery` | Now holds "Free", "Paid" or "Unknown". |

**New columns created:** `Dicount_percentage_(%)` and `delivery_days`.

**Dropped columns:** `price_on_variant`, `sustainability_badges`, `is_best_seller`.

**Columns kept as they were:** `rating`, `number_of_reviews`, `listed_price`, `is_sponsored`, `is_couponed`, `image_url`, `product_url`.

---

## 3. Data Cleaning

### Initial checks
- Looked at the column names, data types and general structure with `df.info()`.
- Counted duplicated rows.
- Calculated the percentage of missing values in each column.

### Converting text to numbers
| Column | What was done |
|---|---|
| `rating` | Text like "4.5 out of 5 stars" was split and only the number was kept. |
| `number_of_reviews` | Thousands separators (commas) were removed and the result converted to numeric. |
| `Revenue_last_month` | Removed the "+" and commas, and replaced "K" with "000" (so "2K+" becomes 2000). Values that still could not be converted became `NaN` using `errors="coerce"`. |
| `Price_after_Discount` | Commas removed, then converted to numeric. |
| `listed_price` | "$" and commas removed. "No Discount" cannot be converted, so it became `NaN`. |
| `price_on_variant` | The price was extracted from the text (the 4th word), "$" and commas removed, then converted to numeric. |

### Filling missing prices
- Missing `Price_after_Discount` values were filled from `price_on_variant`.
- Missing `listed_price` values were filled from `Price_after_Discount`. This is logical because when a product has no discount, the listed price and the price paid are the same. This lowered missing values in `listed_price` from about **72% to about 4.6%**.

### Handling the remaining missing values
- Rows with no `rating` were dropped.
- Missing `Revenue_last_month` values were filled with the column **median**, which is safer than the mean because the data is heavily skewed.
- The remaining missing numeric values were filled with **KNN Imputation** (`KNNImputer`, 4 neighbors), which estimates a missing value from the most similar products.

### Simplifying categorical columns
- `buy_box_availability`: empty values became "Not Available" and "Add to cart" became "Available". The column was renamed `is_available`.
- `is_best_seller` was reduced to a simple `Best_seller` column that keeps only the "Best Seller" label and marks everything else as "No Badge". The original column was then dropped.

### Removing unnecessary columns
- `price_on_variant` was dropped because its information was already captured in the two price columns.
- `sustainability_badges` was dropped because it was mostly empty and inconsistent.

---

## 4. Feature Engineering

### `Dicount_percentage_(%)`
The discount on each product, rounded to one decimal place:

```
(listed_price - Price_after_Discount) / listed_price × 100
```

### `delivery_days`
1. The delivery date (month and day) was extracted from the `delivery_details` text using a regular expression.
2. The year was taken from the collection date and combined with it to build a full date.
3. The number of days between the collection date and the delivery date was calculated, giving the expected delivery time in days.

### `delivery`
The `delivery_details` text was converted into three clean categories:
- **Free**: the text mentions free delivery.
- **Paid**: delivery is not free.
- **Unknown**: there is no delivery information.

---

## 5. Final Dataset Overview

| Column | Type | Description |
|---|---|---|
| `Product_Name` | text | Product title. |
| `rating` | number | Average star rating. |
| `number_of_reviews` | number | Number of customer reviews. |
| `Revenue_last_month` | number | Approximate units sold in the last month. |
| `Price_after_Discount` | number | Price the customer pays. |
| `listed_price` | number | Original price. |
| `Dicount_percentage_(%)` | number | Discount percentage (engineered). |
| `Best_seller` | text | "Best Seller" or "No Badge". |
| `is_sponsored` | text | Sponsored or Organic. |
| `is_couponed` | text | Coupon information. |
| `is_available` | text | Available or Not Available. |
| `delivery` | text | Free, Paid or Unknown. |
| `delivery_days` | number | Days until delivery (engineered). |
| `Order_Placed` | datetime | Date the data was collected. |
| `image_url`, `product_url` | text | Links to the product image and page. |

---

## 6. What Can We Do With This Data?

**Business and market analysis**
- Understand how pricing and discounts relate to sales volume.
- Find which price ranges and discount levels attract the most buyers.
- Measure whether a "Best Seller" badge, a coupon, or sponsored placement is linked to higher sales.
- Study how delivery speed and free shipping affect demand.
- Compare ratings and review counts against sales to understand how customers react to products.

**Machine learning and prediction**
- **Sales prediction:** predict monthly sales from price, discount, rating, reviews, badges and delivery.
- **Rating or popularity prediction:** estimate which products are likely to become best sellers.
- **Price optimization:** suggest a price or discount that balances sales and margin.
- **Clustering:** group similar products or segment the market into budget, mid-range and premium products.
- **Anomaly detection:** spot unusual prices, suspiciously large discounts or abnormal review counts.

**Text and product analysis**
- Apply text analysis (NLP) to `Product_Name` to extract brands, keywords and product categories.
- Use the product URLs and image links to enrich the data with categories or visual features.
- Build a simple product recommendation system based on price, rating and features.

**Business use cases**
- Help sellers decide how to price, discount and promote a new product.
- Help shoppers compare products and find good value deals.
- Support competitor analysis by showing how top products are positioned.

---

## 7. Limitations
- `Revenue_last_month` is an approximate, rounded figure (for example "100+" or "2K+"), so it shows relative demand rather than exact sales.
- Some missing values were estimated (median and KNN imputation), so results involving those fields should be read as approximations.
- The data is a single snapshot taken at one point in time, so it cannot show trends over time.
