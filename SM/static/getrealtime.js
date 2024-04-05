
function updateClock() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    document.getElementById('clock').innerHTML = hours + ':' + minutes + ':' + seconds;
}

setInterval(updateClock, 1000);
updateClock(); // Khởi tạo ngay lập tức để không phải chờ 1 giây đầu tiên
