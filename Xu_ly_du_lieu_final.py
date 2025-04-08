import pandas as pd
import numpy as np
# Đọc dữ liệu từ file CSV
df = pd.read_csv('Intel_CPUs.csv')

# Chọn các cột cần thiết
df = df[['Recommended_Customer_Price', 'nb_of_Cores', 'nb_of_Threads',
         'Cache', 'Bus_Speed', 'Processor_Base_Frequency',
         'Max_Memory_Size', 'Max_Memory_Bandwidth']]

# Xoá các dòng chứa giá trị bị thiếu
df.dropna(inplace=True)
# Đường dẫn tới file Intel_CPUs.csv
file_path = r"C:\Tài liệu học tập\xstk\Intel_CPUs.csv"

# Đọc dữ liệu từ file CSV
data = pd.read_csv(file_path)

# Tùy chỉnh hiển thị
pd.set_option('display.max_rows', 25)  # Hiển thị tối đa 25 dòng
pd.set_option('display.max_columns', 5)  # Hiển thị 5 cột
pd.set_option('display.width', 500)  # Tăng chiều rộng hiển thị để tránh cột bị cắt

# Hiển thị dữ liệu
print(data.head(25))  # Hiển thị 25 dòng đầu tiên
# Hiển thị thông tin chi tiết về dữ liệu
print(data.info())

# Trích xuất các cột quan trọng
columns_to_extract = [
    'Product_Collection', 'Launch_Date', 'Recommended_Customer_Price',
    'nb_of_Cores', 'nb_of_Threads', 'Cache', 'Bus_Speed',
    'Processor_Base_Frequency', 'Max_Memory_Size', 'Max_Memory_Bandwidth'
]
du_lieu_moi = data[columns_to_extract]

# Hiển thị 20 dòng đầu tiên của dữ liệu đã trích xuất
print(du_lieu_moi.head(20))

# Thống kê các giá trị bị khuyết của du_lieu_moi
missing_values = du_lieu_moi.isnull().sum()
print("\nSố lượng giá trị bị khuyết trong mỗi cột:")
print(missing_values)
print(du_lieu_moi[['Product_Collection','Launch_Date', 'Recommended_Customer_Price']].head(20))
du_lieu_moi = du_lieu_moi.dropna(subset=['Launch_Date'])  # Loại bỏ các dòng có Launch_Date bị khuyết

# Định dạng lại cột Launch_Date theo công thức: Số năm + 1 + Số quý
def convert_launch_date(date):
    quarter_mapping = {'1': 0.00, '2': 0.25, '3': 0.50, '4': 0.75}
    quarter = quarter_mapping[date[1]]  # Lấy giá trị quý
    year = int(date[3:].replace("'", "")) + 0  # Lấy năm và chuyển thành số nguyên đầy đủ
    result = year + 1 + quarter
    # Nếu kết quả vượt quá 100, trừ đi 100
    if result >= 100:
        result = result - 100
    return result

du_lieu_moi['Launch_Date'] = du_lieu_moi['Launch_Date'].apply(convert_launch_date)

# Chuẩn hóa cột Product_Collection
def clean_product_collection(value):
    if 'X-series' in value:
        return 'X-series'
    elif 'Celeron' in value:
        return 'Celeron'
    elif 'Pentium' in value:
        return 'Pentium'
    elif 'Quark' in value:
        return 'Quark'
    elif 'Atom' in value:
        return 'Atom'
    elif 'Itanium' in value:
        return 'Itanium'
    elif 'Xeon' in value:
        return 'Xeon'
    elif 'Core m' in value:
        return 'm'
    elif 'Core' in value:
        return 'Core'
    else:
        return value

du_lieu_moi['Product_Collection'] = du_lieu_moi['Product_Collection'].apply(clean_product_collection)

# Hiển thị dữ liệu đã xử lý
print(du_lieu_moi.head(20))
# Xử lý cột Recommended_Customer_Price
def clean_price(value):
    if isinstance(value, str):
        value = value.replace(',', '')  # Loại bỏ dấu phẩy
        if '-' in value:  # Nếu giá trị là khoảng (ví dụ: "$68-$72")
            prices = [float(p.replace('$', '').strip()) for p in value.split('-')]
            return sum(prices) / len(prices)  # Tính trung bình giá trị trong khoảng
        return float(value.replace('$', '').strip())  # Loại bỏ ký hiệu $ và chuyển thành float
    return value

# Áp dụng hàm xử lý cho cột Recommended_Customer_Price
du_lieu_moi['Recommended_Customer_Price'] = du_lieu_moi['Recommended_Customer_Price'].apply(clean_price)

# Tính giá trị trung bình của Recommended_Customer_Price theo từng loại Product_Collection
mean_prices_by_product = du_lieu_moi.groupby('Product_Collection')['Recommended_Customer_Price'].mean()

# Thay thế các giá trị NaN bằng giá trị trung bình tương ứng với Product_Collection
def fill_missing_price(row):
    if pd.isna(row['Recommended_Customer_Price']):  # Nếu giá trị bị khuyết
        return mean_prices_by_product[row['Product_Collection']]  # Thay bằng giá trị trung bình tương ứng
    return row['Recommended_Customer_Price']

du_lieu_moi['Recommended_Customer_Price'] = du_lieu_moi.apply(fill_missing_price, axis=1)

# Hiển thị dữ liệu đã xử lý
print(du_lieu_moi[['Product_Collection','Launch_Date', 'Recommended_Customer_Price']].head(20))


#Xử lý các cột Cache, Bus_Speed, Max_Memory_Size, Max_Memory_Bandwidth

# Hàm chuyển đổi giá trị thành số, loại bỏ đơn vị và xử lý giá trị không hợp lệ
def clean_numeric_column(value, unit_to_remove, conversion_factor=1):
    if isinstance(value, str):
        value = value.replace(unit_to_remove, '').strip()  # Loại bỏ đơn vị
        if value == '' or value.lower() == 'n/a':  # Xử lý chuỗi rỗng hoặc 'N/A'
            return np.nan
    return pd.to_numeric(value, errors='coerce') * conversion_factor  # Chuyển đổi và nhân với hệ số

# Xử lý cột Max_Memory_Bandwidth
du_lieu_moi['Max_Memory_Bandwidth'] = du_lieu_moi['Max_Memory_Bandwidth'].apply(
    lambda x: clean_numeric_column(x, ' GB/s')
)
du_lieu_moi['Max_Memory_Bandwidth'] = du_lieu_moi['Max_Memory_Bandwidth'].fillna(
    du_lieu_moi['Max_Memory_Bandwidth'].mean()
)  # Thay NaN bằng giá trị trung bình

print(du_lieu_moi[['Bus_Speed']].head(20))

# Hàm làm sạch và chuyển đổi giá trị trong cột Bus_Speed
def clean_bus_speed(value):
    if isinstance(value, str):
        value = value.strip()  # Loại bỏ khoảng trắng thừa
        
        # Xử lý các trường hợp đặc biệt
        if value == '' or value.lower() == 'n/a':  
            return np.nan
            
        # Xử lý đơn vị MHz
        if 'MHz' in value:
            try:
                return float(value.replace('MHz', '').strip()) * 1000  # 1 MHz = 1000 KHz
            except ValueError:
                return np.nan
                
        # Xử lý các giao thức DMI/QPI/OPI với đơn vị GT/s
        if 'GT/s' in value:
            try:
                # Loại bỏ các ký tự không cần thiết và giữ lại số
                clean_value = value.replace('GT/s', '').replace('DMI', '').replace('QPI', '').replace('OPI', '').strip()
                base_value = float(clean_value)
                
                # Chuyển đổi dựa trên giao thức
                if 'DMI' in value:
                    return base_value * 500000  # DMI: 1 GT/s = 500000 KHz
                elif 'QPI' in value:
                    return base_value * 500000  # QPI: 1 GT/s = 500000 KHz
                elif 'OPI' in value:
                    return base_value * 500000  # OPI: 1 GT/s = 500000 KHz
                else:
                    return base_value * 500000  # Mặc định cho GT/s
            except ValueError:
                return np.nan
                
    return pd.to_numeric(value, errors='coerce')  # Chuyển đổi thành số hoặc NaN nếu không hợp lệ

# Áp dụng hàm làm sạch cho cột Bus_Speed trước
du_lieu_moi['Bus_Speed'] = du_lieu_moi['Bus_Speed'].apply(clean_bus_speed)

# Tính giá trị trung bình của Bus_Speed theo từng loại Product_Collection
mean_bus_speed_by_product = du_lieu_moi.groupby('Product_Collection')['Bus_Speed'].mean()

# Thay thế các giá trị NaN bằng giá trị trung bình tương ứng với Product_Collection
def fill_missing_bus_speed(row):
    if pd.isna(row['Bus_Speed']):  # Nếu giá trị bị khuyết
        return mean_bus_speed_by_product[row['Product_Collection']]  # Thay bằng giá trị trung bình của loại CPU tương ứng
    return row['Bus_Speed']

# Áp dụng hàm điền giá trị trống
du_lieu_moi['Bus_Speed'] = du_lieu_moi.apply(fill_missing_bus_speed, axis=1)

# Thay thế các giá trị NaN bằng giá trị trung bình của cột
du_lieu_moi['Bus_Speed'] = du_lieu_moi['Bus_Speed'].fillna(du_lieu_moi['Bus_Speed'].mean())

# Hiển thị dữ liệu đã xử lý
print("\nDữ liệu sau khi xử lý cột Bus_Speed:")
print(du_lieu_moi[['Bus_Speed']].head(20))
print(du_lieu_moi.isnull().sum())

# Hàm làm sạch và chuyển đổi giá trị trong cột Processor_Base_Frequency
def clean_processor_frequency(value):
    if isinstance(value, str):
        value = value.strip()  # Loại bỏ khoảng trắng thừa
        if 'GHz' in value:  # Nếu đơn vị là GHz, chuyển đổi sang MHz
            try:
                return float(value.replace('GHz', '').strip()) * 1000
            except ValueError:
                return np.nan
        elif 'MHz' in value:  # Nếu đơn vị là MHz, giữ nguyên giá trị
            try:
                return float(value.replace('MHz', '').strip())
            except ValueError:
                return np.nan
    return pd.to_numeric(value, errors='coerce')  # Chuyển đổi thành số hoặc NaN nếu không hợp lệ

# Áp dụng hàm làm sạch cho cột Processor_Base_Frequency
du_lieu_moi['Processor_Base_Frequency'] = du_lieu_moi['Processor_Base_Frequency'].apply(clean_processor_frequency)

# Thay thế các giá trị NaN bằng giá trị trung bình của cột
du_lieu_moi['Processor_Base_Frequency'] = du_lieu_moi['Processor_Base_Frequency'].fillna(
    du_lieu_moi['Processor_Base_Frequency'].mean()
)

# Hiển thị dữ liệu đã xử lý
print("\nDữ liệu sau khi xử lý cột Processor_Base_Frequency:")
print(du_lieu_moi[['Processor_Base_Frequency']].head(20))

# Kiểm tra xem còn giá trị bị khuyết hay không
missing_values_after = du_lieu_moi['Processor_Base_Frequency'].isnull().sum()
print(f"\nSố lượng giá trị bị khuyết trong cột Processor_Base_Frequency sau khi xử lý: {missing_values_after}")

# Hàm làm sạch và chuyển đổi giá trị trong cột Cache
def clean_cache(value):
    if isinstance(value, str):
        value = value.lower().replace('smartcache', '').replace('l2', '').replace('l3', '').strip()  # Loại bỏ ký tự dư thừa
        if 'mb' in value:  # Nếu đơn vị là MB, chuyển đổi sang KB
            try:
                return float(value.replace('mb', '').strip()) * 1024
            except ValueError:
                return np.nan
        elif 'kb' in value:  # Nếu đơn vị là KB, giữ nguyên giá trị
            try:
                return float(value.replace('kb', '').strip())
            except ValueError:
                return np.nan
        elif value == '' or value == 'n/a':  # Xử lý giá trị rỗng hoặc 'N/A'
            return np.nan
    return pd.to_numeric(value, errors='coerce')  # Chuyển đổi thành số hoặc NaN nếu không hợp lệ

# Áp dụng hàm làm sạch cho cột Cache
du_lieu_moi['Cache'] = du_lieu_moi['Cache'].apply(clean_cache)

# Thay thế các giá trị NaN bằng giá trị trung bình của cột
du_lieu_moi['Cache'] = du_lieu_moi['Cache'].fillna(du_lieu_moi['Cache'].mean())

# Hiển thị dữ liệu đã xử lý

# Kiểm tra xem còn giá trị bị khuyết hay không
missing_values_after = du_lieu_moi['Cache'].isnull().sum()
print(f"\nSố lượng giá trị bị khuyết trong cột Cache sau khi xử lý: {missing_values_after}")

print(du_lieu_moi[['Cache']].head(500))
print(du_lieu_moi.head(20))
print(du_lieu_moi.isnull().sum())

# Xử lý cột nb_of_Threads
du_lieu_moi['nb_of_Threads'] = du_lieu_moi['nb_of_Threads'].fillna(du_lieu_moi['nb_of_Threads'].mean())

# Hàm làm sạch và chuyển đổi giá trị trong cột Max_Memory_Size
def clean_max_memory_size(value):
    if isinstance(value, str):
        value = value.strip()  # Loại bỏ khoảng trắng thừa
        if 'TB' in value:  # Nếu đơn vị là TB, chuyển đổi sang GB
            try:
                return float(value.replace('TB', '').strip()) * 1024  # 1 TB = 1024 GB
            except ValueError:
                return np.nan
        elif 'GB' in value:  # Nếu đơn vị là GB, giữ nguyên giá trị
            try:
                return float(value.replace('GB', '').strip())
            except ValueError:
                return np.nan
        elif value == '' or value.lower() == 'n/a':  # Xử lý chuỗi rỗng hoặc 'N/A'
            return np.nan
    return pd.to_numeric(value, errors='coerce')  # Chuyển đổi thành số hoặc NaN nếu không hợp lệ

# Áp dụng hàm làm sạch cho cột Max_Memory_Size
du_lieu_moi['Max_Memory_Size'] = du_lieu_moi['Max_Memory_Size'].apply(clean_max_memory_size)

# Thay thế các giá trị NaN bằng giá trị trung bình của cột Max_Memory_Size
du_lieu_moi['Max_Memory_Size'] = du_lieu_moi['Max_Memory_Size'].fillna(du_lieu_moi['Max_Memory_Size'].mean())

# Hiển thị dữ liệu đã xử lý
print("\nDữ liệu sau khi xử lý cột nb_of_Threads và Max_Memory_Size:")
print(du_lieu_moi[['nb_of_Threads', 'Max_Memory_Size']].head(20))

# Kiểm tra xem còn giá trị bị khuyết hay không
missing_values_after = du_lieu_moi[['nb_of_Threads', 'Max_Memory_Size']].isnull().sum()
print(f"\nSố lượng giá trị bị khuyết trong các cột sau khi xử lý:\n{missing_values_after}")

# Kiểm tra kết quả
print(du_lieu_moi.head(50))
print(du_lieu_moi.isnull().sum())



# Tính các giá trị đặc trưng cho các biến định lượng
quantitative_columns = [
    'Launch_Date', 'Recommended_Customer_Price', 'nb_of_Cores', 'nb_of_Threads',
    'Processor_Base_Frequency', 'Cache', 'Bus_Speed', 'Max_Memory_Size', 'Max_Memory_Bandwidth'
]

# Tạo DataFrame chứa các giá trị đặc trưng
stats_df = pd.DataFrame({
    'mean': du_lieu_moi[quantitative_columns].mean(),
    'sd': du_lieu_moi[quantitative_columns].std(),
    'median': du_lieu_moi[quantitative_columns].median(),
    'Q1': du_lieu_moi[quantitative_columns].quantile(0.25),
    'Q3': du_lieu_moi[quantitative_columns].quantile(0.75),
    'min': du_lieu_moi[quantitative_columns].min(),
    'max': du_lieu_moi[quantitative_columns].max()
})

# Thống kê số lượng cho biến phân loại Product_Collection
product_collection_counts = du_lieu_moi['Product_Collection'].value_counts()




# Định dạng hiển thị số thập phân với 2 chữ số sau dấu phẩy
pd.options.display.float_format = '{:.2f}'.format
print(du_lieu_moi['Bus_Speed'].head(20))
# Hiển thị lại bảng thống kê các giá trị đặc trưng
print("\nBảng thống kê các giá trị đặc trưng :")
pd.set_option('display.max_columns', None)  # Hiển thị tất cả các cột
print(stats_df)
# Hiển thị số lượng cho biến phân loại Product_Collection
print("\nThống kê số lượng cho Product_Collection:")
print(product_collection_counts)
import pandas as pd
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Đọc dữ liệu từ file CSV
data = pd.read_csv('Intel_CPUs.csv')

# Xử lý dữ liệu
data['Recommended_Customer_Price'] = data['Recommended_Customer_Price'].apply(
    lambda x: float(x.replace(',', '').replace('$', '').strip()) if isinstance(x, str) else x
)
data = data[['Recommended_Customer_Price', 'nb_of_Cores', 'nb_of_Threads', 'Cache', 'Bus_Speed', 'Processor_Base_Frequency', 'Max_Memory_Size', 'Max_Memory_Bandwidth']]
data.dropna(inplace=True)

# Chọn cột đặc trưng và cột mục tiêu
X = data[['nb_of_Cores', 'nb_of_Threads', 'Cache', 'Bus_Speed', 'Processor_Base_Frequency', 'Max_Memory_Size', 'Max_Memory_Bandwidth']]
y = data['Recommended_Customer_Price']

# Thêm cột hệ số chặn cho mô hình hồi quy
X = sm.add_constant(X)

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Xây dựng mô hình hồi quy tuyến tính với statsmodels
model = sm.OLS(y_train, X_train).fit()

# In kết quả tóm tắt của mô hình
print(model.summary())

# Dự đoán giá trị trên tập kiểm tra
y_pred = model.predict(X_test)

# Đánh giá mô hình
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# In hệ số của mô hình với tên các biến
coefficients = model.params
print('\nCoefficients:')
for i, col in enumerate(X.columns):
    print(f'{col}: {coefficients[i]}')

print(f'\nIntercept: {model.params[0]}')

# Kiểm tra một số dự đoán
print('True values:', y_test.head().values)
print('Predicted values:', y_pred[:5])
