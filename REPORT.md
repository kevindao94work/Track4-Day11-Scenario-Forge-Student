MSSV: 2A202602793

# Lab 11 · Scenario Forge — báo cáo

Thị trấn được tạo cho MSSV này là **B** (`evidence/meta.json: _run.town`). Các kết quả dưới đây dùng ngân sách đầy đủ, không dùng `--quick` (`evidence/meta.json: _run.quick = false`; các bước có `quick = false`).

## 1. Phát lại log có trung thực không? (bước A)

| Chỉ số | Kết quả |
|---|---:|
| Kịch bản lấy mẫu / log bị loại vì người lái va chạm | 400 / 1 |
| Còn lại để so sánh | 399 |
| Va chạm khi phát lại log | 124: `rear` 113, `side` 11 |
| Va chạm trong thế giới phản ứng | 1: `front` 1 |
| Va chạm có ở cả hai | 1 |

Nguồn: `evidence/replay.json: n`, `dropped_human_crash_logs`, `n_used`, `replay`, `reactive`, `crash_in_both`.

Phần lớn va chạm `rear` là giả vì xe phía sau trong log bị đóng băng theo quỹ đạo người lái cũ; nó không phản ứng với việc planner phanh sớm hoặc đổi quỹ đạo. Ví dụ kịch bản `2` trong `replay_only`: khi các xe phản ứng bình thường không xảy ra va chạm và TTC tối thiểu là 2.576 giây, nhưng phát lại log gây va chạm phía sau. Đây là khác biệt giữa log phản thực và giao thông có phản ứng, không phải bằng chứng rằng planner chắc chắn gây ra vụ va chạm đó (`evidence/replay.json: replay_only[0]`).

## 2. Kịch bản bất khả thi (bước B)

| Luật trong `is_feasible` | Căn cứ |
|---|---|
| `cutDur` phải hữu hạn và dương | Thời lượng chuyển làn bằng không hoặc không hợp lệ không mô tả được chuyển động vật lý. |
| `(π / cutDur)² × 3.5 / 2 ≤ μg` | Gia tốc ngang cực đại của chuyển làn 3,5 m không được vượt độ bám đường. |
| `cutBrake ≤ μg` | Lực phanh dọc không thể vượt giới hạn ma sát đường. |
| `pedV ≤ 2.5 m/s` | Loại tốc độ chạy khỏi mô hình người đi bộ. |
| `0 < cutV ≤ 22 m/s` | Tốc độ xe nhập làn phải dương và trong giới hạn mô hình. |
| Các giá trị cần dùng phải hữu hạn, có đủ khóa và đổi được sang số | Dữ liệu sai định dạng không thể được xem là kịch bản vật lý hợp lệ. |

Trong bốn cuộc săn, `crosswalk_block` có nhiều mẫu bất khả thi nhất: 11; tiếp theo là `rear_ended` 6, `bus_bypass` 3 và `cut_in` 3 (`evidence/hunt.json: <mode>.infeasible`). CEM tối ưu điểm nguy hiểm trên các mẫu khả thi, nhưng phân phối đề xuất vẫn có thể lấy mẫu gần các biên vật lý, nhất là khi các tham số thời gian, tốc độ và phanh thay đổi đồng thời. Mẫu bị loại không được mô phỏng và không được cập nhật như va chạm.

Nếu cộng nhầm 16 mẫu bất khả thi của Monte Carlo vào 11 va chạm thật, ta sẽ báo `(11 + 16) / 3000 = 0.009` thay vì `11 / 3000 = 0.00367`. Đây chỉ là phép tính minh họa sai lệch; kết quả chính thức không tính mẫu bất khả thi là va chạm (`evidence/mc.json: crashes`, `infeasible`, `n`).

## 3. Monte Carlo cho bạn biết gì (bước C1)

`evidence/mc.json` có `k = 11`, `n = 3000`, `p̂ = 0.003667` và khoảng Wilson 95% `[0.002049, 0.006554]`. Dùng xấp xỉ lập kế hoạch `1.96² p(1-p) / (0.2p)²`, cần khoảng **26.097 lần chạy** để nửa độ rộng gần bằng 20% của `p̂`; đây là mục tiêu xấp xỉ quanh ước lượng hiện tại, không phải bảo đảm chính xác của khoảng Wilson.

Không quan sát thấy `cut_in`, `rear_ended` và `other`. Với mỗi kiểu, con số phải báo là `k = 0 / 3000` cùng cận trên Wilson 95% `0.001279`, không phải xác suất bằng 0 (`evidence/mc.json: per_mode`).

## 4. Importance sampling, ESS và độ suy biến (bước C3)

Mỗi ô dùng 600 mẫu cho một kiểu và một seed. `top_share` là phần tổng trọng số va chạm do mẫu va chạm có trọng số lớn nhất đóng góp.

| Kiểu | Seed | `p` | `hits` | `ess` | `top_share` |
|---|---:|---:|---:|---:|---:|
| `bus_bypass` | 0 | 1.904e-3 | 54 | 123.4 | 0.618 |
| `bus_bypass` | 1 | 3.220e-4 | 58 | 120.8 | 0.299 |
| `bus_bypass` | 2 | 3.693e-3 | 55 | 135.7 | 0.552 |
| `cut_in` | 0 | 0 | 0 | 128.2 | 0 |
| `cut_in` | 1 | 0 | 0 | 141.0 | 0 |
| `cut_in` | 2 | 0 | 0 | 106.1 | 0 |
| `crosswalk_block` | 0 | 1.698e-6 | 70 | 113.4 | 0.462 |
| `crosswalk_block` | 1 | 5.640e-6 | 78 | 140.4 | 0.403 |
| `crosswalk_block` | 2 | 1.477e-4 | 74 | 125.8 | 0.989 |
| `rear_ended` | 0 | 0 | 0 | 116.6 | 0 |
| `rear_ended` | 1 | 0 | 0 | 128.2 | 0 |
| `rear_ended` | 2 | 0 | 0 | 122.8 | 0 |

Nguồn mọi hàng: `evidence/estimate.json: seeds[i].per[mode]`. Ba seed bất đồng đáng kể: tổng lần lượt là `0.001905`, `0.000328` và `0.003841`; ước lượng Monte Carlo là `0.003667`. Riêng `bus_bypass` trải từ `0.000322` đến `0.003693`; `crosswalk_block` từ `1.70e-6` đến `1.48e-4`. Vì vậy các tổng IS chưa ổn định giữa seed, dù seed 2 gần với Monte Carlo hơn.

`top_share > 0.5` ở `bus_bypass` seed 0 và 2, và `crosswalk_block` seed 2 (0.989). Trong các trường hợp đó, một mẫu chi phối gần như toàn bộ tổng trọng số; một sự kiện hiếm được gán trọng số quá lớn khiến kết quả nhạy với seed và phân phối đề xuất. Các kiểu không có hit có `upper_zero_hits = 0.025`: đây là quy tắc 3 lần số mẫu từ thành phần tự nhiên của hỗn hợp phòng vệ, tức `3 / (β × 600) = 3 / 120`, không phải `3 / 600` và cũng không phải điểm ước lượng 0 (`evidence/estimate.json: seeds[i].per[mode].upper_zero_hits`).

`other` không được săn riêng: đây là nhóm dư không đồng nhất, không có một bề mặt nguy hiểm riêng được định nghĩa; phần này lấy từ Monte Carlo. `evidence/estimate.json: other` ghi `0 / 3000`, `p = 0`, nguồn `mc.json`, cận trên `0.001279`. Ngân sách IS là 16.800 mẫu tổng cộng (`evidence/estimate.json: budget`), thấp hơn khoảng 26.097 mẫu Monte Carlo cần cho mục tiêu tương đối 20%; nhưng ESS chỉ khoảng 106–141 trên 600 và `top_share` cao làm giảm đáng kể độ tin cậy thực tế của một số ước lượng. Không nên kết luận IS đạt độ chính xác tương đương chỉ dựa vào tổng ngân sách.

## 5. Các kiểu thất bại (bước C2 + 3D)

Hai kiểu va chạm thật được tìm thấy là `bus_bypass` và `crosswalk_block`. Tôi chạy chẩn đoán độc lập bằng `avsim.core.rollout` trên đúng tham số trong `evidence/viewer.json`. Ở mẫu `B-01`, xe ego không nhìn thấy người đi bộ (`ped-visible = 0`) khi tiếp cận xe buýt đang dừng; xe `C2` nhập làn sát xe buýt và va chạm với ego ở 12,5 giây. Ở mẫu `C-01`, người đi bộ `P1` đi qua lối sang đường; đầu xe ego dừng gần vạch nhưng còn lấn vào đường đi bộ, và sự kiện `block` xảy ra ở 19,2 giây khi ego đứng yên. Tham số thật được lưu tại `evidence/viewer.json: runs[id=B-01]` và `runs[id=C-01]`.

Ảnh chụp 3D thật hiện chưa có trong `evidence/shots/`. Lần thử mở `viewer/index.html` trong công cụ trình duyệt bị chặn ngay ở giao thức cục bộ với lỗi `URL protocol not allowed`; danh sách bề mặt tự động hóa cũng không có tab trình duyệt để thao tác. Trước đó viewer báo `THREE.WebGLRenderer: Error creating WebGL context`, nhưng lỗi mở file hiện tại không cho phép kiểm tra lại context hay kết luận GPU của Safari/Chrome bị lỗi. Máy có GPU Apple M4, Safari 27.2 và Chrome 155; trạng thái WebGL/tăng tốc phần cứng khi chạy chưa thể kiểm tra trong công cụ tự động hóa. `evidence/shots/README.md` hướng dẫn kiểm tra Chrome tại `chrome://gpu`. `evidence/shots/README.md` ghi các bước mở viewer trực tiếp và lệnh chụp thủ công cho hai kiểu lỗi, ảnh so sánh planner và cảnh xe đạp. Không dùng ảnh dựng thay thế.

Các cuộc săn `bus_bypass` và `crosswalk_block` tìm lần lượt 199 và 37 ca đúng kiểu; cuộc săn `cut_in` chỉ tìm 36 ca `bus_bypass`, còn cuộc săn `rear_ended` tìm 8 ca `crosswalk_block` và 1 ca `bus_bypass`. Không có va chạm `cut_in` hay `rear_ended` trong các kết quả săn (`evidence/hunt.json: <mode>.found`). Đây là bằng chứng yếu về việc chưa tìm thấy, không chứng minh các kiểu đó không thể xảy ra. Một cuộc săn chung có thể dồn mẫu vào vùng đang cho điểm nguy hiểm cao nhất và bỏ sót vùng khác; các kết quả `found` lệch kiểu trong hai cuộc săn trên cho thấy rủi ro đó.

## 6. Sửa planner (bước E + 3D)

Chính sách được chọn trên TRAIN là thay `cutinLat` từ 2.15 lên 3.0; các núm khác giữ mặc định (`evidence/fix.json: chosen.policy`, `baseline_test.policy`). Chỉ số bên dưới lấy từ TEST độc lập.

| Chính sách | `fail` | `fail_hi_seen` | `fail_hi` hợp lệ | `progress` (m) | `harsh` trung bình |
|---|---:|---:|---:|---:|---:|
| Được chọn (`cutinLat=3.0`) | 5.93e-7 | 1.07e-6 | 0.03878 | 214.63 | 7.864 |
| Gốc | 0.001688 | 0.004472 | 0.005751 | 214.78 | 8.248 |

Nguồn: `evidence/fix.json: chosen_test` và `baseline_test`; `progress` là quãng đường trung bình tới va chạm hoặc hết hành trình, `harsh` là số khung phanh gấp trung bình. Chính sách được chọn không có va chạm `bus_bypass` trong TEST nên đánh dấu kiểu này là `unseen`; cận trên 0-hit của nó là 0.0375. Vì thế `fail_hi` của chính sách mới lớn hơn `fail` điểm của chính sách gốc dù ước lượng điểm của nó thấp hơn. Đây là so sánh giữa cận trên có tính bất định và ước lượng điểm, không phải bằng chứng rằng bản sửa tệ hơn hoặc tốt hơn chắc chắn. Cận `fail_hi` của bản sửa rộng hơn cả cận của gốc; TEST chưa đủ để khẳng định ưu thế thống kê.

Tôi kiểm tra lại tình huống `B-01` với cùng tham số: chính sách gốc va chạm `ego–C2` ở 12,5 giây, còn `cutinLat=3.0` không có va chạm. `evidence/viewer.json` lưu chính sách đã chọn để viewer vẽ bóng mờ cho các ca tìm thấy dưới chính sách gốc. Ảnh có bóng mờ chưa được chụp vì công cụ tự động hóa bị chặn truy cập `file://`; xem cách chụp trực tiếp trong `evidence/shots/README.md`. Các ứng viên đã thử không cho thấy núm nào “nghe an toàn hơn” nhưng làm tăng thất bại một cách nhất quán; tôi không suy diễn hiệu ứng phản trực giác khi không có bằng chứng đo được.

## 7. Từ mô phỏng ra đường thật

| Giả định trong thị trấn B | Dữ liệu thật cần thay thế | Nếu giả định lệch |
|---|---|---|
| Khoảng trống xe nhập làn `cutGap` có trung vị 12 m, phân phối log-normal (`avsim/space.py: Natural.cut_gap_median`, `CONT`) | Video đã hiệu chỉnh theo mét hoặc dữ liệu quỹ đạo từ xe/camera tại các điểm nhập làn; đo khoảng cách và tốc độ tương đối lúc xe quyết định nhập. | Nếu tài xế ngoài đời chấp nhận khe nhỏ hơn, mô hình có thể đánh giá thấp số lần nhập làn sát và rủi ro; khe lớn hơn có thể khiến mô hình đánh giá cao rủi ro. Hướng và độ lớn còn phụ thuộc phản ứng các xe khác. |
| 30% mẫu là đường ướt, `μ=0.5` khi ướt và `μ=0.8` khi khô (`avsim/space.py: VARIANTS[B]`, `to_params`) | Nhật ký mưa/độ ướt theo chuyến ghép với phép đo ma sát mặt đường tại khu vực và mùa tương ứng. | Tỷ lệ ướt thực hoặc độ giảm ma sát lớn hơn giả định có thể làm mô hình đánh giá thấp rủi ro phanh/đổi làn; nếu đường khô hơn hoặc bám tốt hơn, mô hình có thể đánh giá cao. |
| Người đi bộ ngó qua xe buýt với xác suất 0.85; khoảng thời gian chấp nhận `pedGap` có trung vị 4.5 giây (`avsim/space.py: BIN`, `CONT`) | Video nhiều ngày ở điểm dừng xe buýt và vạch qua đường, gán nhãn che khuất, hướng nhìn, thời điểm bắt đầu sang đường và khe thời gian đến xe. | Nếu tỷ lệ ngó qua thấp hơn hoặc người đi bộ chấp nhận khe ngắn hơn, họ có thể bước ra khi xe đến gần hơn và rủi ro thật tăng so với mô hình; nếu họ quan sát thường xuyên hơn hoặc chờ khe lớn hơn, mô hình có thể đánh giá cao. |

Đây là các giả định giảng dạy, chưa được hiệu chỉnh bằng dữ liệu giao thông thực (`avsim/space.py` ghi rõ). Các hướng sai lệch trên là suy luận có điều kiện, không phải kết quả đo tại địa phương.

## 8. Giới hạn

1. Thế giới mô phỏng có một cấu hình đường và giao lộ cố định; không đại diện được đầy đủ cho hình học đường, biển báo và hành vi ưu tiên khác.
2. Xe khác tuân theo các luật chuyển động và IDM đơn giản, còn người đi bộ dùng quy tắc thời điểm/khoảng trống cố định; chúng không bao quát đa dạng phản ứng của người thật.
3. Cảm biến và nhận thức gần như hoàn hảo ngoài che khuất được mô hình hóa quanh xe buýt; lỗi phân loại, mưa trên camera, vật cản khác và sai lệch định vị không được lấy mẫu đầy đủ.

Trong một tuần tiếp theo, tôi sẽ thu quỹ đạo có thời gian đồng bộ tại một điểm dừng xe buýt và vạch sang đường trong cả giờ cao điểm và thấp điểm; gán nhãn ít nhất khe nhập làn, độ ướt, tầm nhìn/ngó qua và khe người đi bộ chấp nhận; sau đó so sánh phân phối đo được với giả định mô phỏng và chạy lại ước lượng rủi ro cùng khoảng tin cậy. Chỉ sau bước kiểm định đó mới có cơ sở điều chỉnh các tham số tự nhiên.

## 9. Rắc rối của bạn (bước G + chương 10)

**Rắc rối:** xe đạp cùng chiều đi sát mép phải làn E2, tiếp cận xe buýt đang dừng rồi lạng trái vào hành lang E1 để vượt qua xe buýt khi xe ego đến gần. Đây là một giới hạn có thể kiểm tra của planner: quỹ đạo xe đạp cắt ngang hành lang ego, dù xe đạp bắt đầu giảm tốc sau xe buýt. Cảnh cụ thể trong `hazard.json` không va chạm; lỗi chỉ xuất hiện khi quét dải tham số trong giao thông của thị trấn.

**Căn cứ và cấu hình:** tôi giữ định dạng `avsim-studio/1` cùng `params`, `policy` và `ego` của tệp đã xuất từ chương 10; thẻ `bike` và dải quét theo đúng schema trong `avsim/studio.py` và `viewer/sim-core.js`. Vị trí xe buýt dừng ban đầu xấp xỉ 106 m trên E2 (`BUS s=326`; xe đạp dùng `h0_x+220`). Dải `h0_x=85–90 m` đặt xe đạp sau xe buýt, cách tâm xe buýt 16–21 m; đó là đoạn sau giao lộ x=80 m và trước xe buýt trên bản đồ mô phỏng. Dải này tránh chồng lấn giữa xe đạp và xe buýt ở đầu lượt và cho phép xe đạp giảm tốc trước khi lạng vượt. Xe đạp đi 4–6 m/s (14,4–21,6 km/h); độ lệch ban đầu 1,0–1,4 m đưa xe tới gần mép phải E2; cú lạng 3,3–4,1 m trong 2,7–3,5 s hướng sang E1. Gia tốc ngang cực đại ở góc bất lợi nhất là 2,78 m/s², thấp hơn giới hạn 3 m/s² của `studio.BIKE_LAT_MAX`. Thời điểm 0–2 s và ngưỡng kích hoạt 10–30 m là dải kiểm tra. Các khoảng `space` là thiết kế bao phủ khi lấy mẫu đều, không phải phân phối tần suất ngoài đời.

Tôi loại dải ban đầu `x=195–225 m` vì nằm xa hơn vị trí ego thường tới trong lượt mô phỏng, nên xe đạp không kích hoạt và không tạo phép thử hữu ích. Tôi cũng loại dải thử `x=90–120 m`: dải đó chứa vị trí trùng với xe buýt dừng tại x≈106 m và gây chồng lấn ban đầu ở nhiều mẫu. Dải cuối `x=85–90 m` không có chồng lấn ở frame 0; điều này được xác nhận qua `mine.json: baseline.overlap_at_start` và `chosen.overlap_at_start`, cả hai bằng 0.

Không có khảo sát thực địa để ước lượng tần suất tình huống, nên `hazard.json: exposure = null`. Không đưa ra tỷ lệ lỗi mỗi chuyến. `mine` lấy mẫu đều trong `space`; kết quả là xác suất có điều kiện trên dải tham số kiểm tra và phân phối giao thông mô phỏng của thị trấn B, không phải xác suất thực địa.

**Kết quả đủ ngân sách:** cảnh cụ thể không va chạm (`evidence/mine.json: exact.planner = []`). Có `1.490/1.500` mẫu khả thi, tỷ lệ chấp nhận `0,9933`; 10 mẫu bất khả thi không được chạy và không được tính là lỗi. Cả baseline lẫn policy được chọn đều dùng cùng 1.490 mẫu:

| Chính sách | Va chạm ego | `avoidable` | `unavoidable` | `unattributed` | Va chạm ở tốc độ <1 m/s | `avoidable_foreknown` | p̂ tránh được, có điều kiện [Wilson 95%] |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gốc | 385 | 382 | 3 | 0 | 34 | 384 | 0,2564 [0,2349; 0,2792] |
| Được chọn (`cutinLat=3.0`) | 302 | 297 | 5 | 0 | 157 | 302 | 0,1993 [0,1798; 0,2204] |

Nguồn: `evidence/mine.json: accepted`, `baseline`, `chosen`; policy được chọn trong `evidence/fix.json: chosen_test.policy`. Mọi va chạm ego được quy cho xe đạp (`H0`); không có va chạm `unattributed`. Trên chính dải quét này, planner được chọn có ít va chạm và ít lỗi `avoidable` hơn planner gốc, nhưng có nhiều va chạm khi ego gần như đứng yên (157 so với 34). Đây là so sánh mô tả trong bộ mô phỏng/dải đã chọn, không phải bằng chứng về tần suất ngoài đời hay bảo đảm planner tốt hơn trên mọi tình huống.

`avoidable` nghĩa là phanh hết cỡ từ khung đầu xe ego nhìn thấy xe đạp đã tránh được va chạm. Đây là chuẩn lạc quan cho khả năng phanh: nó giả sử phản ứng tức thời và phanh tối đa, nên các ca này là cận trên của lỗi có thể tránh bằng phanh thực tế. Phép thử chỉ dùng phanh, không thử đánh lái, nên có thể bỏ sót đường thoát mà một planner có thể tìm bằng đổi hướng. `avoidable_foreknown` còn giả định biết rắc rối ngay khi nó bắt đầu, kể cả khi bị che; vì vậy nó không thay cho `avoidable` theo tầm nhìn thực tế. Trong sweep này có 384 ca baseline và 302 ca policy mới tránh được theo giả định biết trước; chênh lệch với `avoidable` là ảnh hưởng của việc chưa nhìn thấy ngay.

**Ảnh và tự lái:** ảnh thật của chương 9/10 chưa được chụp do giới hạn truy cập `file://` của công cụ trình duyệt, như câu 5. Các lệnh và mốc phát lại để chụp trực tiếp nằm trong `evidence/shots/README.md`. Tôi chưa thực hiện lái thủ công.

**Cách sửa:** thay đổi đã chọn trong Lab 11 là tăng `cutinLat` từ 2,15 lên 3,0 m, giúp planner tính xe lấn sang hành lang sớm hơn. Nó giảm lỗi có thể tránh trong sweep này nhưng không loại bỏ lỗi và đi kèm nhiều va chạm tốc độ thấp; cần thêm logic dự đoán quỹ đạo ngang của xe đạp và một hành động né/phanh phối hợp. Đề xuất này chưa được cài đặt hay đánh giá. Muốn đổi kết quả có điều kiện thành rủi ro mỗi chuyến, cần đo tần suất xe đạp vượt xe buýt tại vị trí tương ứng bằng video/quỹ đạo thực địa trước, không gán một `exposure` giả định.
