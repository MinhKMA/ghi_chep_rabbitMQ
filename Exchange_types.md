# Các loại Exchange

## Direct Exchange

Một direct exchange cung cấp các messages tới queues dựa trên một message routing key. Routing key là một thuộc thuộc tính của mesage được thêm vào message header từ producer. Routing key có thể được xem là một địa chỉ mà Exchange sử dụng để định tuyến các messages. **A message goes to the queue(s) whose binding key exactly matches the routing key of the message.**

Direct exchange được sử dụng trong trường hợp bạn muốn phân biệt các messages published cho cùng một exchange bằng cách sử dụng một chuỗi định danh đơn giản.

Exchange mặc định của AMQP brokers phải cung cấp cho direct exchange là `amq.direct`.

<img src="https://i.imgur.com/2sjgr6H.png">

- SCENARIO 1
    + Exchange: pdf_events
    + Queue A: create_pdf_queue
    + Binding key between exchange (pdf_events) and Queue A (create_pdf_queue): pdf_create
- SCENARIO 2
    + Exchange: pdf_events
    + Queue B: pdf_log_queue
    + Binding key between exchange (pdf_events) and Queue B (pdf_log_queue): pdf_log

- Ví dụ:

    Một message với routing key `pdf_log` được gửi từ exchange `pdf_events`. Message đó được định tuyến tới pdf_log_queue vì outing key (pdf_log) khớp với binding key (pdf_log).

    Nếu message routing key không khớp với binding key nào thì sẽ bị hủy bỏ.

## Default exchange

Exchange mặc định là một pre-declared direct exchange không có định danh(tên) thương được biểu diễn bởi một chuỗi rỗng `""`.

Khi bạn sử dụng exchange mặc định, message của bạn được gửi đến queue có tên chính là routing key của message. Tất cả queue tự động được liên kết với exchange mặc định kèm với một routing key giống như tên của queue. 

## Topic Exchange

Topic exchanges định tuyến các messages tới queues được trên đối chiếu, đối sánh ky tự (wildcard matches) giữa routing key và cái gì đó được gọi là mẫu định tuyến được chỉ định bởi queue binding. Messages được định tuyến tới một hoặc nhiều queues được trên một đối sánh giữa một routing key của message và this pattern. 

routing key phải là một danh sách của các từ(a list of words) phân cách bởi dấu chấm (.) ví dụ `agreements.us` và `agreements.eu.stockholm` trong trường hợp này xác định các thỏa thuận được thiết lập cho một công ty có văn phòng ở nhiều địa điểm khác nhau. routing patterns có thể chứa dấu hoa thị("*") để đối sánh một từ ở một vị trí cụ thể của routing key (ví dụ: một routing pattern của chuỗi "agreements.*.*.b.*" chỉ match routing keys ở từ đầu tiên là "agreements" và một từ thứ tứ là "b"). Ký tự thăng (#) cho biết match với zero hoặc nhiều từ hơn(ví dụ một routing pattern của "agreements.eu.berlin.#" matches với bất cứ routing keys bắt đầu với "agreements.eu.berlin") 

consumers biểu diễn topic mà họ quan tâm như đăng kí để có một nguồn dữ liệu cho từng thẻ riêng biệt

Consumers tạo ra một queue và thiết lập một binding với một với một mẫu định tuyến đã cho tới exchange. Tất cả message với một routing key khớp với routing pattern được định tuyến đến queue và ở đó đến khi consumers đến lấy message

Mặc định của exchange AMQP brokers phải cung cấp cho  topic exchange là `amq.topic`.

<img src="https://i.imgur.com/ZlMqg0R.png">

- SCENARIO 1
    
    The image to the right show an example where consumer A is interested in all the agreements in Berlin.

    + Exchange: agreements
    + Queue A: berlin_agreements
    + Routing pattern between exchange (agreements) and Queue A (berlin_agreements): agreements.eu.berlin.#
    + Example of message routing key that matches: agreements.eu.berlin and agreements.eu.berlin.headstore
- SCENARIO 2
    Consumer B is interested in all the agreements.

    - Exchange: agreements
    - Queue B: all_agreements
    - Routing pattern between exchange (agreements) and Queue B (all_agreements): agreements.#
    - Example of message routing key that matches: agreements.eu.berlin and agreements.us
￼
-  SCENARIO 3
    Consumer C is interested in all agreements for European head stores.

    + Exchange: agreements
    + Queue C: headstore_agreements
    + Routing pattern between exchange (agreements) and Queue C (headstore_agreements): agreements.eu.*.headstore
    + Example of message routing keys that will match: agreements.eu.berlin.headstore and agreements.eu.stockholm.headstore

Ví dụ:

Một message có routing key `agreements.eu.berlin` được gửi tới exchange agreements. Message được đính tuyến đến queue `berlin_agreements` bởi vì routing pattern của "agreements.eu.berlin.#" match với bất kì routing key nào bắt đầu là "agreements.eu.berlin". Tin nhắn cũng được định tuyến đến queue `all_agreements` vì routing key (agreements.eu.berlin) match routing pattern (agreements.#)

## Fanout Exchange

Fanout copy và định tuyến một mesage nhận được tới tất cả queue được ràng buộc với nó.

Fanout Exchange được dùng trong trường hợp khi một hoặc nhiều thông điệp được gửi tới một hoặc nhiều queues với nhiều consumers có thể xử lý cùng một message the o nhiều cách khác nhau. 

Mặc định là "amq.fanout".

<img src="https://i.imgur.com/Zq7asE9.png">

- SCENARIO 1
    + Exchange: sport_news
    + Queue A: Mobile client queue A
    + Binding: Binging between the exchange (sport_news) and Queue A (Mobile client queue A)

Ví dụ: 

Một mesage được gửi đến exchange `sport_news`. Message đó được định tuyến tới tất cả các queues (Queue A, Queue B, Queue C) 