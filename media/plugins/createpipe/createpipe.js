


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
     $("#Y_id").html (yzminfo['id']);
     $("#Y_name").html (yzminfo['name']);
     $("#Y_desc").html (yzminfo['desc']);
     $("#Y_image_url").html (yzminfo['image_url']);
     document.getElementById('Y_img').src='http://127.0.0.1:8000/media/'+yzminfo['img'];
     $("#Y_add_time").html (yzminfo['add_time']);
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

