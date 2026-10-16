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

Ảnh chụp 3D thật không có trong thư mục nộp: chính sách bảo mật trình duyệt đã chặn việc mở tiếp viewer cục bộ, và không cho phép chuyển sang đường mở khác để lấy ảnh. Tôi không tạo ảnh thay thế. Vì vậy phần ảnh chụp cho cả hai kiểu còn thiếu.

Các cuộc săn `bus_bypass` và `crosswalk_block` tìm lần lượt 199 và 37 ca đúng kiểu; cuộc săn `cut_in` chỉ tìm 36 ca `bus_bypass`, còn cuộc săn `rear_ended` tìm 8 ca `crosswalk_block` và 1 ca `bus_bypass`. Không có va chạm `cut_in` hay `rear_ended` trong các kết quả săn (`evidence/hunt.json: <mode>.found`). Đây là bằng chứng yếu về việc chưa tìm thấy, không chứng minh các kiểu đó không thể xảy ra. Một cuộc săn chung có thể dồn mẫu vào vùng đang cho điểm nguy hiểm cao nhất và bỏ sót vùng khác; các kết quả `found` lệch kiểu trong hai cuộc săn trên cho thấy rủi ro đó.

## 6. Sửa planner (bước E + 3D)

Chính sách được chọn trên TRAIN là thay `cutinLat` từ 2.15 lên 3.0; các núm khác giữ mặc định (`evidence/fix.json: chosen.policy`, `baseline_test.policy`). Chỉ số bên dưới lấy từ TEST độc lập.

| Chính sách | `fail` | `fail_hi_seen` | `fail_hi` hợp lệ | `progress` (m) | `harsh` trung bình |
|---|---:|---:|---:|---:|---:|
| Được chọn (`cutinLat=3.0`) | 5.93e-7 | 1.07e-6 | 0.03878 | 214.63 | 7.864 |
| Gốc | 0.001688 | 0.004472 | 0.005751 | 214.78 | 8.248 |

Nguồn: `evidence/fix.json: chosen_test` và `baseline_test`; `progress` là quãng đường trung bình tới va chạm hoặc hết hành trình, `harsh` là số khung phanh gấp trung bình. Chính sách được chọn không có va chạm `bus_bypass` trong TEST nên đánh dấu kiểu này là `unseen`; cận trên 0-hit của nó là 0.0375. Vì thế `fail_hi` của chính sách mới lớn hơn `fail` điểm của chính sách gốc dù ước lượng điểm của nó thấp hơn. Đây là so sánh giữa cận trên có tính bất định và ước lượng điểm, không phải bằng chứng rằng bản sửa tệ hơn hoặc tốt hơn chắc chắn. Cận `fail_hi` của bản sửa rộng hơn cả cận của gốc; TEST chưa đủ để khẳng định ưu thế thống kê.

Tôi kiểm tra lại tình huống `B-01` với cùng tham số: chính sách gốc va chạm `ego–C2` ở 12,5 giây, còn `cutinLat=3.0` không có va chạm. `evidence/viewer.json` lưu chính sách đã chọn để viewer vẽ bóng mờ cho các ca tìm thấy dưới chính sách gốc. Tuy nhiên ảnh chụp viewer thật bị giới hạn như mô tả ở câu 5, nên chưa có ảnh bóng mờ để nộp. Các ứng viên đã thử không cho thấy núm nào “nghe an toàn hơn” nhưng làm tăng thất bại một cách nhất quán; tôi không suy diễn hiệu ứng phản trực giác khi không có bằng chứng đo được.

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

**Rắc rối:** xe đạp đi cùng chiều ở mép phải làn E2 rồi lạng vào phía làn E1 khi xe ta đến gần. Ngoài đời, tình huống tương tự có thể xảy ra khi người đi xe đạp né ổ gà hoặc vật cản ở lề đường. Tôi dùng tệp gốc `avsim-studio/1` đã xuất từ chương 10; bản xuất ban đầu không có thẻ rắc rối. Vì trình duyệt chặn thao tác sửa trong viewer, tôi giữ nguyên `format`, `params`, `policy` và `ego` của bản xuất, rồi thêm thẻ `bike` cùng ba trường thí nghiệm theo đúng schema trong `avsim/studio.py` và `viewer/sim-core.js`. Đây là phần mở rộng theo schema đã kiểm chứng, không phải ảnh chụp hay bản xuất nguyên trạng sau khi dựng thẻ trong giao diện.

**Căn cứ và giả định:** giả thuyết ban đầu là cú lạng vào gần xe đang chạy có thể làm planner phát hiện muộn. `hazard.json: space` thay đổi vị trí `195–225 m`, độ lệch ngang `1.0–1.4 m`, tốc độ `4–7 m/s`, độ lạng `3.3–4.1 m`, thời lượng lạng `2.7–3.5 s`, thời điểm `0–2 s` và ngưỡng kích hoạt `10–30 m`. Dải này nằm trong giới hạn của `studio.LIMITS`; gia tốc ngang cực đại ở góc bất lợi nhất là `2.78 m/s²`, dưới ngưỡng `3 m/s²`. `hazard.json: exposure = 0.01` là giả định kỹ thuật minh họa, tương ứng một lần trong 100 chuyến; chưa có khảo sát địa phương để xác nhận tần suất. `hazard.json: why` ghi rõ căn cứ và tình trạng chưa đo này.

**Kết quả:** `evidence/mine.json: exact.planner = []`, nên cảnh gốc không có va chạm. Quét đầy đủ có 1.490/1.500 mẫu khả thi (`accepted = 0.9933`).

| Chính sách | `crashes` | `avoidable` | `avoidable_foreknown` | `unavoidable` | `unattributed` | `low_speed` |
|---|---:|---:|---:|---:|---:|---:|
| Gốc | 5 | 0 | 0 | 0 | 5 | 0 |
| Được chọn | 0 | 0 | 0 | 0 | 0 | 0 |

Nguồn: `evidence/mine.json: accepted`, `baseline` và `chosen`. Cả hai chính sách có `n = 1490`. Năm va chạm dưới policy gốc đều là sự cố giao thông thường với `C2`, xảy ra trước khi xe đạp hoạt động; vì vậy chúng được ghi là `unattributed`, không phải lỗi do rắc rối xe đạp. Với cả hai policy, xác suất lỗi planner có điều kiện trên rắc rối là `0 / 1490 = 0`, khoảng Wilson 95% `[0, 0.002572]`. Cận trên theo mỗi chuyến là `0.01 × 0.002572 = 0.0000257`; điểm ước lượng là 0, không có nghĩa xác suất thật bằng 0.

Để so sánh quy mô, Monte Carlo tự nhiên ghi nhận `bus_bypass = 10 / 3000 = 0.003333` mỗi chuyến, với khoảng Wilson 95% `[0.001812, 0.006125]` (`evidence/mc.json: per_mode.bus_bypass`). Cận trên mỗi chuyến của rắc rối xe đạp thấp hơn ước lượng điểm đó, nhưng so sánh phụ thuộc giả định `exposure = 0.01` và hai sự kiện có định nghĩa khác nhau; đây không phải tần suất thực địa.

**Hình và tự lái:** không có ảnh chụp thật của chương 9/10 do giới hạn bảo mật trình duyệt đã nêu ở câu 5. Tôi chưa thực hiện lái thủ công.

**Cách sửa:** các lần chạy không ghi nhận va chạm nào do xe đạp lạng, nên dữ liệu này không ủng hộ việc đổi một núm planner cụ thể cho tình huống đó. Để tăng độ bao phủ ngoài dải đã thử, planner có thể cần dự đoán quỹ đạo ngang của xe đạp và giảm tốc sớm khi hướng lạng cắt vào hành lang xe; đây là đề xuất thiết kế, chưa phải hiệu quả đã đo.
