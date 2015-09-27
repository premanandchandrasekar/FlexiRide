var list_booked;
//Server url to connect socket
var URL = 'http://localhost:5001/sockjs';

var options = {protocols_whitelist: ['xdr-streaming', 'xhr-streaming', 'iframe-eventsource', 'xdr-polling', 'xhr-polling','iframe-xhr-polling','jsonp-polling'], debug: true, jsessionid: false};

var socket = new SockJS(URL, null, options);

socket.onopen = function () {
	console.log('Connection open');
};

socket.onclose = function() {
     console.log('Connection closed');
};

socket.onmessage = function(message) {
    console.log('Socket_Connection_message', message.data);
	var data = JSON.parse(message.data);
	list_booked = data.bookedcabs_list;
	if(data.inserted){
		var inserted_detials = data.details;
		var template = _.template($("#pending_details_template").html());
				$("#pending_details").prepend(template({'driver_name': inserted_detials.driver_name,
													'cab_number':inserted_detials.cab_number,
													'driver_number':inserted_detials.driver_mobile_number,
													'crn_id':'crn'+inserted_detials.crn,
													'crn':inserted_detials.crn,
													'crn':'arrived'+inserted_detials.crn,
													'estimated_time':inserted_detials.estimated_time}));
	}
	else{
	if(data.bookedcabs_list){
		for(var i=0;i<data.bookedcabs_list.length;i++){
			var crn_id = data.bookedcabs_list[i]['crn']
			var prev_val = $('#'+crn_id).html();
			var in_sec = prev_val * 60;
			var new_val = in_sec - 6;			
			var in_min = new_val/60;
			$('#'+crn_id).html('');
			$('#'+crn_id).text(in_min);
			secondPassed(in_sec,crn_id);
			//$("#total_Organization").html("").append(data.org);
		}
	}
}
    
};

function secondPassed(seconds,crn) {
    var minutes = Math.round((seconds - 30)/60);
    var remainingSeconds = seconds % 60;
    if (minutes <= 0) {
          $('#crn'+crn).html('');
          $('#crn'+crn).text('Arrived');
    }
    else{
    	$('#crn'+crn).html('');
    	$('#crn'+crn).text(minutes + "min:" + remainingSeconds+"sec");
    }
}

function show_booked_cabs(booked_cabs){
	if (booked_cabs.length != 0){
		var template = _.template($("#pending_details_template").html());
		for(var i=0;i<booked_cabs.length;i++){
			$("#pending_details").append(template({'driver_name': booked_cabs[i].driver_name,
													'cab_number':booked_cabs[i].cab_number,
													'driver_number':booked_cabs[i].driver_mobile_number,
													'crn_id':'crn'+booked_cabs[i].crn,
													'crn':booked_cabs[i].crn,
													'estimated_time':booked_cabs[i].estimated_time}));
		}
	}

}

$(function(){
setInterval(function(){
	if(list_booked != undefined){
	if(list_booked.length != 0){
		for(var i=0;i<list_booked.length;i++){
			var crn_id = list_booked[i]['crn']
			var text = $('#crn'+crn_id).html();
			if (text=='Arrived' && text != undefined){
				$('#crn'+crn_id).parent().html('');
				var template = _.template($("#pending_details_template").html());
				$("#complated_details").append(template({'driver_name': list_booked[i].driver_name,
													'cab_number':list_booked[i].cab_number,
													'driver_number':list_booked[i].driver_mobile_number,
													'crn_id':'arrivedcrn'+list_booked[i].crn,
													'crn':'arrived'+list_booked[i].crn,
													'estimated_time':'Arrived'}));
			}
		}
	}
}
},3000);
});

$(document).ready(function() {
    $.get('/api/latest/bookedcabsdetails').error(function(res) {
        }).then(function(res){
        	if (res.success){
        		show_booked_cabs(res.booked_cabs_lists);
        	}
        });
});