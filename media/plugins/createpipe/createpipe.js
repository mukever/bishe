


$(document).ready(function () {

    var yzmid = document.getElementById("yzmname").value;

    getyzminfo(yzmid);

});


var getyzminfo=function(id){
    $.ajax({
            url: "http://127.0.0.1:8000/api/getyzminfo/"+id,
            type: 'GET',
            async: true,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                putdaratohtml(data)
            },
            error: function () {
                console.log("error");
            }

        });
}


var putdaratohtml=function(yzminfo){
    console.log("处理html")
        console.log(yzminfo['yzmname']['img'])
     $("#Y_name").html (yzminfo['yzmname']['name']);
     $("#Y_desc").html (yzminfo['yzmname']['desc']);
     $("#Y_image_url").html (yzminfo['yzmname']['image_url']);
     document.getElementById('Y_img').src='http://127.0.0.1:8000/media/'+yzminfo['yzmname']['img'];
     $("#Y_add_time").html (yzminfo['yzmname']['add_time']);
    console.log("赋值完成");

}

$("#yzmname").change(function(){
    console.log("改修选取");
    var yzmid = document.getElementById("yzmname").value;

    getyzminfo(yzmid);
});

$("#TestBtn").click(function () {
    console.log("测试按钮点击");
    var yzmid = document.getElementById("yzmname").value;
    console.log(yzmid);

})

