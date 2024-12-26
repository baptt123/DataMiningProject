// Lấy nút Scroll to Top
var scrollTopBtn = document.getElementById("scrollTopBtn");

// Hiển thị nút khi người dùng cuộn xuống 100px
window.onscroll = function() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollTopBtn.style.display = "block";
    } else {
        scrollTopBtn.style.display = "none";
    }
};

// Khi người dùng nhấp vào nút, cuộn trang lên đầu
scrollTopBtn.onclick = function() {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}
