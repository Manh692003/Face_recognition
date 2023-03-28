# Máy chấm công

Chương trình nhân diện khuôn mặt bằng OpenCV

- Chương trình này thực hiện nhận diện khuôn mặt sử dụng thư viện face_recognition và OpenCV. 
- Đọc tệp pickle chứa danh sách các mã hóa khuôn mặt đã biết từ trước. Sau đó, tiến hành quét khung hình hiện tại từ máy ảnh để tìm kiếm khuôn mặt.
  - Nếu tìm thấy một khuôn mặt, chương trình sẽ so sánh mã hóa khuôn mặt đó với danh sách mã hóa đã biết từ trước để xác định xem đó là ai. Nếu khuôn mặt được nhận dạng là của một sinh viên, đoạn code sẽ hiển thị thông tin sinh viên trên màn hình và tăng số lần dự sự kiện của sinh viên đó lên 1. 
  - Đồng thời, đoạn code sẽ lưu lại thời gian cuối cùng mà sinh viên đó tham gia sự kiện trong cơ sở dữ liệu Firebase.
