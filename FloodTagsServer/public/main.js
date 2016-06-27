function start_algorithm(){
    source = document.getElementById("stream").value;
    frame =document.getElementById("frame").value;
    loop = document.getElementById("loop").value;

    $.ajax({
        dataType: "json",
        url: "/dashboard/start_algorithm?source=" + source + "&frame=" + frame + "&loops=" + loop,
        data: null,
        success: function (data) {
            console.log("yay")
            location.href = "/dashboard"
        }
    });
}