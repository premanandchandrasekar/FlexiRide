Webcam.attach('#webcam');

Webcam.set({
    width: 640,
    height: 480,
    dest_width: 640,
    dest_height: 480,
});

flag = true

function take_snapshot() {
    var data_uri = Webcam.snap();
    Webcam.upload(data_uri, "api/latest/camupload", function(code, res) {
        res = JSON.parse(res);
        $("#textcam").html(res.text);
        if(res.id != "none"){
            $("#idcard").html(res.id);
        }
        flag = true;
    } );

}

window.setTimeout(function(){
    window.setInterval(function(){
        if(flag){
            flag = false;
            take_snapshot();
        }
    }, 100);
}, 5000);

