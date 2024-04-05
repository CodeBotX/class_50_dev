var marksTable = document.getElementById("marks-table");
var marks = [];
for (var i = 0; i < marksTable.rows.length - 1; i++) { // Lặp qua các hàng chứa điểm
    var markText = marksTable.rows[i].cells[1].innerText;
    var markValue = parseFloat(markText.replace(/[^\d.-]/g, '')); // Loại bỏ tất cả các ký tự không phải là số, dấu chấm hoặc dấu trừ
    if (!isNaN(markValue)) { // Kiểm tra nếu giá trị là số hợp lệ
        marks.push(markValue);
    }
}

// Tính điểm trung bình
function calculateAverage(marks) {
    if (marks.length === 0) {
        return null;
    }
    var total = marks.reduce((acc, curr) => acc + curr, 0);
    return total / marks.length;
}

// Hiển thị điểm trung bình
var averageMark = calculateAverage(marks);
var averageMarkElement = document.getElementById("average-mark");
if (averageMark !== null) {
    averageMarkElement.innerText = averageMark.toFixed(2);
} else {
    averageMarkElement.innerText = "N/A";
}