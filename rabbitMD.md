# Định nghĩa về RabbitMQ
RabbitMQ là một phần mềm quản-lý-hàng-đợi message, thường được gọi là môi-giới-message hay trình-quản-lý-message. Nói đơn giản, đây là phần mềm định nghĩa hàng đợi một ứng dụng khác có thể kết nối đến để bỏ message vào và gửi message dựa trên nó.

# Tại sao lại sử dụng RabbitMQ
Nếu muốn các thành phần này giao tiếp được với nhau thì chúng phải biết nhau. Nhưng điều này gây rắc rối cho việc viết code. Một thành phần phải biết quá nhiều đâm ra rất khó maintain, debug. Giải pháp ở đây là thay vì các liên kết trực tiếp, khiến các thành phần phải biết nhau thì sử dụng một liên kết trung gian qua một message broker. Với sự tham gia của message broker thì producer sẽ không hề biết consumer. Nó chỉ việc gửi message đến các queue trong message broker. Consumer chỉ việc đăng ký nhận message từ các queue này.

Vì producer nói chuyện với consumer trung gian qua message broker nên dù producer và consumer có khác biệt nhau về ngôn ngữ thì giao tiếp vẫn thành công. Dù viết bằng java, python, php hay ruby... thì chỉ cần thỏa mãn giao thức với message broker là có thể nói chuyện được với nhau. 

Một đặc tính của rabbitmq là asynchronous. Producer không thể biết khi nào message đến được consumer hay khi nào message được consumer xử lý xong. Đối với producer, đẩy message đến message broker là xong việc. Consumer sẽ lấy message về khi nó muốn. 

# Một flow để gửi-nhận message trong RabbitMQ

<img src="https://i.imgur.com/x04r63q.png">

- Producer đẩy message vào exchange. Khi tạo exchange, bạn phải mô tả nó thuộc loại gì. Các loại exchange sẽ được giải thích trong một bài khác.
- Sau khi exchange nhận message, nó chịu trách nhiệm định tuyến message. Exchange sẽ chịu trách về các thuộc tính của message, ví dụ routing key, phụ thuộc loại exchange.
- Việc binding phải được tạo từ exchange đến hàng đợi. Trong trường hợp này, ta sẽ có hai binding đến hai hàng đợi khác nhau từ một exchange. Exchange sẽ định tuyến message vào các hàng đợi dựa trên tuộc tính của của từng message.
- Các message nằm ở hàng đợi đến khi chúng được xử lý bởi một consumer
- Consumer xử lý message

## Các loại Exchange

<img src="https://i.imgur.com/1L62LhB.png">

- **Direct**: Một Direct exchange sẽ đẩy message đến hàng đợi dựa theo khóa định tuyến – routing key. Ví dụ, nếu hàng đợi gắn với một exchange có binding key là pdfprocess, message được đẩy vào exchange với routing key là pdfprocess sẽ được đưa vào hàng đợi.

    ```sh
    Routing key: Là một khóa mà exchange dùng nó để quyết định cách đưa vào hàng đợi. Routing key có thể hiểu như một địa chỉ của message.
    ```

- **Fanout**: Một Fanout exchange sẽ đẩy message đến toàn bộ hàng đợi gắn với nó.
- **Topic**: Một topic exchange sẽ làm một lá bài (gọi là wildcard) để gắn routing key với một routing pattern khai báo trong binding
- **Header**: Một header exchange sẽ dùng các thuộc tính header của message để định tuyến.

# Một ví dụ 

<img src="https://i.imgur.com/xEdejul.png">

    ```sh
    Producer: tạo ra các message và đẩy chúng lên broker
    Consumer: kết nối đến hàng đợi này và theo dõi các message để xử lý
    ```

Kiến trúc cơ bản của một hàng đợi message khá đơn giản, có các ứng dụng client được gọi producer để tạo ra các message và đẩy chúng lên broker (môi giới message). Các ứng dụng khác được gọi là consumer, kết nối đến hàng đợi này và theo dõi các message để xử lý. Phần mềm có thể là một producer, hay consumer hoặc cả hai. Message sẽ được giữ trong hàng đợi đến khi consumer lấy chúng đi.
