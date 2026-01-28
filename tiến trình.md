# **SESSION  1: Khởi động \+ Thực hành cơ bản với bonbanh.com** 

| Thời gian | Nội dung | Hoạt động | Ghi chú |
| :---- | :---- | :---- | :---- |
| **0-15'** | Website Reverse Engineering |  \- Phân biệt:  Server Side Rendering Client Side Rendering Hybrid & Protected   \- Bản chất của browser là hiển thị và render content cho user | Giống như đi nhà hàng sang trọng (Fine Dining). Các em ngồi vào bàn (Gửi Request), đầu bếp nấu nướng, bày biện xong xuôi ra đĩa rồi phục vụ mới mang ra Trả về HTML đầy đủ. Cách nhận diện cũng rất đơn giản**,** Bấm Ctrl \+ U (View Source) là thấy hết html content. Client Side Rendering (CSR) Đầu bếp chỉ cho các em cái nồi lẩu và cái bếp (Khung HTML rỗng). Sau đó, nhân viên chạy bàn (JavaScript) mới chạy đi lấy thịt, rau (JSON Data) về thả vào nồi, Cách nhận diện thì cũng vô cùng đơn giản, đối ngược với SSR thì nó cũng là CSR \===  Demo chút |
| **30-45'** | Thực hành với Bonbanh.com | Bước 1: Phân tích mục tiêu: https://bonbanh.com/oto/honda-city-cu Sau đó Inspect chỉ vào: \-Tên xe (Thẻ h3, itemprop='name'). \-Giá xe (Thẻ b, itemprop='price'). \-Thông tin năm/nơi bán (Thẻ div, class cb2\_02). Bước 2: Code Python (Live Coding \- 20 phút) | Hướng dẫn Demo crawl một trang, sau đó cho bài tập crawl 10 trang liên tục mà và lưu data lại |

# **SESSION 2: Data và làm việc với SSR bằng Selenium \- Cafef**

| Thời gian | Nội dung | Hoạt động | Ghi chú  |
| :---- | :---- | :---- | :---- |
| **0-10'** | Đặt vấn đề: Tại sao requests thất bại? | Tiếp tục phân tích cấu trúc website cafef, trang lịch sử giao dịch VNINDEX | Yêu cầu sinh viên: Thử làm cái request như cũ xem thử có thể lấy được data như trang bonbanh.com  Demo chạy đoạn code requests nhanh. Kết quả: Không tìm thấy thẻ \<table\> hoặc tìm thấy bảng rỗng. Đây chính là CSR, khi requests tải trang về, nó chỉ nhận được Khung HTML. Còn nội dung được Javascript tải về sau đó 1-2 giây. requests không biết đợi, nên nó về tay không. \-\> Giải pháp**:** Cần một phương pháp biết "đợi". Đó là **Selenium**. |
| **10-15'** | Setup Môi trường trên Colab | \# 1\. Cài đặt các gói cần thiết trên máy chủ Linux của Google \!apt-get update \!apt-get install \-y chromium-chromedriver \!cp /usr/lib/chromium-browser/chromedriver /usr/bin \# 2\. Cài thư viện Selenium \!pip install selenium |  |
| **30-40'** | Live Coding |  | Có thể nâng cao, demo tính năng bấm nút của selenium |

# **SESSION 3: Data và làm việc với SSR bằng API request \- Cafef**

| Thời gian | Nội dung | Hoạt động | Ghi chú |
| :---- | :---- | :---- | :---- |
| **0-2’** | Đặt vấn đề: Tại sao Selenium nên là lựa chọn cuối cùng? |  Ưu điểm: Dễ hiểu. Nhược điểm: Quá chậm (phải tải cả ảnh, quảng cáo, màu sắc...), tốn RAM, dễ lỗi nếu web đổi giao diện. \==== Ưu điểm: Cực nhanh (chỉ lấy chữ, không lấy ảnh), dữ liệu sạch, có cấu trúc. Nhược điểm: Phải tìm được số điện thoại kho hàng (API Endpoint) và có mật khẩu (Headers/Cookies). |  |
| **5-15'** | Giới thiệu Dev tools | Cần cho sinh viên hiểu rõ về dev tools, cách mà ứng dụng tách ra hai phần frontend và backend | Yêu cầu SV gửi link form cho bạn bên cạnh điền thử (Test chéo). |
| **15-20'** | Live Coding  |  |  |

### **SESSION 4: Data và làm việc với SSR bằng API request nâng cao**

| Thời gian | Nội dung | Hoạt động | Ghi chú |
| :---- | :---- | :---- | :---- |
| **0-10'** | Đặt vấn đề: Tại sao Selenium nên là lựa chọn cuối cùng?   | Demo Truy cập trang shopee, trang sẽ block nếu chúng ta không đăng nhập  | Đáp ứng LO: "Chức năng nhập liệu vào hệ thống". |
| **10-15’** | Thực hành tìm kiếm gói tin chứa thông tin khi tìm kiếm  |  |  |
| **15-30’** | Giới thiệu postman và các thành phần bên trong API, Live Coding |  |  |

