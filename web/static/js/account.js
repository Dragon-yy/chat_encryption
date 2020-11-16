$(function () {
    // 回车触发按钮点击事件
    // $(document).keyup(function (event) {
    //     if (event.keyCode == 13) {
    //         $("#userAccount").trigger("click");
    //     }
    // });
    $(document).on("click", ".userAccount", function (e) {
        alert('a')
    });
    $('#userAccount').click(function (event) {
        window.location.href = "account";
    })
});