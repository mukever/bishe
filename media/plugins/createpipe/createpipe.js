


$(document).ready(function () {

    var yzmid = document.getElementById("yzmname").value;

    getyzminfo(yzmid);
    getpixelinfo();

});


var getyzminfo=function(id){
    $.ajax({
            url: "http://127.0.0.1:8000/api/getyzminfo/"+id,
            type: 'GET',
            async: false,
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
        console.log(yzminfo['yzmname'])
     $("#Y_name").html (yzminfo['yzmname']['name']);
     $("#Y_desc").html (yzminfo['yzmname']['desc']);
     $("#Y_image_url").html (yzminfo['yzmname']['image_url']);
     document.getElementById('Y_img').src='/media/'+yzminfo['media_img'];
     $("#Y_add_time").html (yzminfo['yzmname']['add_time']);
    console.log("赋值完成");

}


var getpixelinfo = function(){

    console.log("开始渲染验证码图像像素信息");

    $.ajax({
            url: "http://127.0.0.1:8000/api/getyzmpixelinfo/",
            type: 'GET',
            async: false,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                putpixelinfotohtml(data);
            },
            error: function () {
                console.log("error");
            }

        });

}

var putpixelinfotohtml = function(data){

    document.getElementById('Y_imgpixelinfo').src='/media/'+data['pixel'];
    document.getElementById('Y_imgpixelinfogray').src='/media/'+data['pixelgray'];


}


$("#Y_Submit").click(function () {
    getimgcutinfo()
})


var getimgcutinfo= function(){

    console.log("开始切分验证码");
    var label = $("#img_label").val();
    console.log(label);
    label = 'test';

    if(label ==""){
        alert("请输入Label");
    }else {
        $.ajax({
            url: "http://127.0.0.1:8000/api/getyzmcutinfo/",
            type: 'POST',
            data:{'label':label,'neednumber':4},
            async: false,
            dataType: 'json',
            success: function (data) {
                console.log(data);
                var box = document.getElementById("cutInfo");
                document.getElementById("cutInfo").innerHTML = "";
                for(var i=0;i<data['cut'].length;i++){
                     var box = document.getElementById("cutInfo");
                    var span = document.createElement('img')
                    span.src = '/media/'+data['cut'][i]
                    span.setAttribute('class','col-sm-3')
                    span.setAttribute('height',200)
                    span.style.setProperty('border-color','red')
                    var textLabel = document.createElement('label')
                    // textLabel.innerText = '第'+(i+1)+'切分状态';
                    // span.appendChild(textLabel)
                    box.appendChild(span)
                    // document.getElementById('Y_cut'+i).src='/media/'+data['cut'][i];
                }
            },
            error: function () {
                console.log("error");
            }

        });

    }


}


$("#yzmname").change(function(){
    console.log("改修选取");
    var yzmid = document.getElementById("yzmname").value;
    getyzminfo(yzmid);
    getpixelinfo()
});


