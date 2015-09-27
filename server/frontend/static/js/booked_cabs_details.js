function show_booked_cabs(booked_cabs){
	if (booked_cabs.length != 0){
		console.log('222222222222222222');
	}

}


$(document).ready(function() {
    $.get('/api/latest/bookedcabsdetails').error(function(res) {
            console.log(res);
        }).then(function(res){
        	if (res.success){
        		show_booked_cabs(res.booked_cabs_lists);
        	}
        });
});