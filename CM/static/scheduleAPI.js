document.addEventListener('DOMContentLoaded', function() {
    // Phân tích URL để lấy classroom_name
    var pathArray = window.location.pathname.split('/');
    var classroomName = pathArray[2]; // Điều chỉnh chỉ số dựa trên cấu trúc URL của bạn

    var apiUrl = `/home/${classroomName}/schedule_api`;

    function fetchData() {
        var now = new Date();
        var timeStr = now.toTimeString().split(' ')[0]; // Định dạng HH:MM:SS

        fetch(`${apiUrl}?time=${timeStr}`)
            .then(response => response.json())
            .then(data => {
                // Xác định vị trí để cập nhật DOM dựa trên dữ liệu nhận được
                var updateElement = document.getElementById('update-element-id'); // Thay 'update-element-id' bằng ID của phần tử bạn muốn cập nhật

                if (data.message) {
                    updateElement.innerText = data.message;
                } else {
                    updateElement.innerText = `Period: ${data.current_period}, Subject: ${data.subject}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Xử lý lỗi
            });
    }

    fetchData(); 
    setInterval(fetchData, 5000); // Cập nhật mỗi 5 giây
});
