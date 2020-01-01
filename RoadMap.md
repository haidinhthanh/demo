## Các bước thực hiện dự án:

### Bước 1: Thu thập thông tin:

- Crawl các bài báo trên intertet dựa trên 1 số query trên search engine như: "thu hút nhân tài", "đào tạo nhân tài",  "giữ chân nhân tài", "nguồn lực chất lượng cao"
- Lấy các dữ liệu thô từ các link bài báo: title, headline (abstract), content, source, published_date, images
- Lưu dữ liệu vào elasticsearch index (dùng md5 hash của url làm id). Cần học cách index, query, thiết lập mapping các document trên nền tảng elasticsearch để phục vụ việc dễ dàng truy query, aggregate data. 

### Bước 2: Phân tích, xử lý thông tin:

Xây dựng các modul xử lý dữ liệu. Các bài báo "thô" sẽ được xử lý qua 1 data pipleline gồm các bước:

- Phát hiện bài báo không liên quan  (Filter Processor): nếu bài báo không liên quan gì đến vấn đề "nhân tài", "nhân lực", quá ít nội dung (video) thì lọc bỏ.
- Phát hiên trùng lặp (Deduplication Processor): nếu 2 bài báo có nội dung rất giống nhau, ko mang lại thêm thông tin mới cho người dùng thì được nhóm vào làm 1
- Phát hiện các thông tin về địa điểm nhắc đến trong bài báo (Geo Name Recognition): Ví dụ như các tỉnh thành ở Việt Nam hay Các Quốc gia trên thế giới.
- Phát hiện các lĩnh vực nhắc đến trong bài báo (Categorization): Ví dụ Giáo dục, Công nghệ, Tài chính, Thể thao, Y tế, Nông nghiệp.....
- Phát hiện các vấn đề liên quan đến thu hút nhân tài trong bài báo: Ví dụ Mức lương, Môi trường làm việc, Chính sách, Chế độ

Cuối bước này các bài báo qua xử lý được lưu vào một elasticsearch index mới để để phân tích và tìm kiếm. Sinh viên cần tìm hiểu một số thực viện hỗ trợ NER. Ví dụ https://spacy.io/api/entityrecognizer hay một thư viện phù hợp với việc xử lý tiếng Việt.

### Bước 3: Xuất bản thông tin:

Lấy các bài báo từ bước 3 tự động gửi lên 1 site dùng wordpress API. Yêu cầu tổ chức cách trình thông tin cho đẹp mắt, dễ hiểu, đễ tìm và phân tích thông tin. 

### Lưu ý:

- Tại mỗi bước Sinh viên cố gắng chọn một phương pháp đơn giản nhất làm để đảm bảo hệ thống chạy được từ end-to-end. Nếu có thời gian mới tập trung vào cải tiến, so sánh chất lượng với các phương pháp, thư viện khác.
- Các code nên thường xuyên push lên github để nhận được review và góp ý
- Các tài sản trí tuệ của dự án (code, dữ liệu, thông tin truy cập hệ thống) không chia sẻ, bán cho bên thứ 3 nếu không có sự trao đổi và đồng ý của giáo viên và người đồng hướng dẫn.
