$(document).ready(function(){
    var params = {'pickup_lat':12.97189, 'pickup_lng':77.64115};
    $.get('/api/latest/fetch/available/cabs', params).error(function(res) {
            console.log(res);
        }).then(function(res){
            console.log(res);
        });
});