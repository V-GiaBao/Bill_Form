document.addEventListener("DOMContentLoaded", function () {
    const dateInput = document.querySelector("input[type='date']");
    const today = new Date();
    dateInput.value = today.toISOString().split("T")[0];
});

// function themBenh() {
//     // Lấy giá trị từ ô nhập liệu
//     const diseaseInput = document.getElementById("disease-input").value.trim();
//     const resultInput = document.getElementById("disease-txt");
//     const existingDiseases = resultInput.value.split(",").map(item => item.trim());
//     // Kiểm tra nếu giá trị rỗng
//     if (diseaseInput === "") {
//         alert("Vui lòng nhập một loại bệnh!");
//         return;
//     }

    // Kiểm tra nếu giá trị đã tồn tại
//     if (existingDiseases.includes(diseaseInput)) {
//         alert("Loại bệnh này đã có trong danh sách!");
//     } else {
//         // Thêm giá trị mới vào danh sách
//         resultInput.value = existingDiseases.filter(item => item !== "").concat(diseaseInput).join(", ");
//     }
//
//     // Xóa nội dung ô nhập liệu
//     document.getElementById("disease-input").value = "";
// }

// function xoaBenh() {
//     const resultInput = document.getElementById("disease-txt");
//     const existingDiseases = resultInput.value.split(",").map(item => item.trim());
//     existingDiseases.pop(); // Loại bỏ phần tử cuối cùng
//     resultInput.value = existingDiseases.join(", ").trim(); // Cập nhật ô kết quả
// }

// function themThuoc() {
//     const newMedItem = document.createElement("div");
//     newMedItem.className = "row med-item pb-sm-2";
//
//     // Nội dung bên trong div mới
//     newMedItem.innerHTML = `
//             <div class="col-sm-3 text-center">
//                   <input type="text" name="medicine" list="medicineList">
//                   <datalist id="medicineList">
//                     {% for t in thuocs %}
//                     <option value="{{ t.TenThuoc }}">
//                     {% endfor %}
//                   </datalist>
//             </div>
// <!--            <div class="col-sm-2 text-center">-->
// <!--                <input type="text" id="med-unit" name="med-unit" class="border" placeholder="Đơn vị" onkeydown="return false">-->
// <!--            </div>-->
//             <div class="col-sm-7 text-center">
//                 <input type="text" id="med-instruct" name="med-instruct" class="border" placeholder="Cách dùng">
//             </div>
//             <div class="col-sm-2 text-center">
//                 <input type="text" id="med-number" name="med-number" class="border" placeholder="Số lượng">
//             </div>
//       `;
    // Thêm div mới vào container
    // document.getElementById("med-container").appendChild(newMedItem);
// }

let counter = 1; // Biến đếm bắt đầu từ 1
function themThuoc() {

    const newMedItem = document.createElement("div");
    newMedItem.className = `row med-item pb-sm-2`;

    // Nội dung bên trong div mới
    newMedItem.innerHTML = `
            <div class="col-sm-3 text-center">
                  <input type="text" name="medicine${counter}" list="medicineList">
                  <datalist id="medicineList">     
<!--                    <option value="Thuốc Độc">-->
<!--                    <option value="Thuốc Giải">-->
                    {% for t in thuocs %}
                        <option value="{{ t.TenThuoc }}">
                    {% endfor %}
                  </datalist>
            </div>
            <div class="col-sm-7 text-center">
                <input type="text" id="med-instruct${counter}" name="med-instruct${counter}" class="border med-instruct${counter}" placeholder="Cách dùng">
            </div>
            <div class="col-sm-2 text-center">
                <input type="text" id="med-number${counter}" name="med-number${counter}" class="border med-number${counter}" placeholder="Số lượng">
            </div>  
      `;

    // Thêm div mới vào container
    document.getElementById("med-container").appendChild(newMedItem);

    // Tăng giá trị của counter để các lớp lần sau được cập nhật
    counter++;
}

function xoaThuoc() {
    const medItems = document.querySelectorAll("#med-container .med-item");
    // Kiểm tra nếu có hơn một phần tử
    if (medItems.length > 1) {
        const lastMedItem = medItems[medItems.length - 1];
        lastMedItem.remove();
    }
}