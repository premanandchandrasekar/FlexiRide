$(document).ready(function(){
    
    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');
 
        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
    });

    $("#search_button").click(function(e){
        var mob_no = $("#search_key").val();
        if((mob_no.length > 0) && (mob_no.length==10)){
            $("#ps_container").hide();
        } else if(mob_no.length > 0 && mob_no.length < 10){
            $("#error_msg").text("Enter a valid 10 digit mobile number.").css('color', '#f9aa0b').show().fadeOut(2000);
            return;
        } else if(mob_no.length==0){
            $("#ps_container").show();
        }
        $("html, body").animate({ scrollTop: $('#booking_header').offset().top }, 1000);
    });

});


//[Start google places autocpmplete]
//Autocomplete destination with latitude and longitude.
var autocomplete;

function initAutocomplete() {
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
      /** @type {!HTMLInputElement} */(document.getElementById('destination')),
      {types: ['geocode']});
  autocomplete.addListener('place_changed', fillInLatLong);
}

function fillInLatLong() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  var latitude = place.geometry.location.lat().toFixed(6);
  var longitude = place.geometry.location.lng().toFixed(6);
  document.getElementById('destination').setAttribute('data-lat', latitude);
  document.getElementById('destination').setAttribute('data-long', longitude);
  getEstimatedFare(latitude, longitude, place);
}
//[End google places autocpmplete]

function getEstimatedFare(latitude, longitude, place){
    latitude = parseFloat(latitude);
    longitude = parseFloat(longitude);
    console.log(parseFloat(latitude));
    console.log(typeof(latitude));
    var params = {'pickup_lat':12.917582, 'pickup_lng':77.623128, 'drop_lat':latitude, 'drop_lng':longitude};
    $.get('/api/latest/fetch/available/cabs', params).error(function(res) {
        console.log(res);
    }).then(function(res){
        console.log(res);
        if(res.success){
            var data = res.data;
            var template = _.template($('#cabDetails').html());
            $('#cabDetailsTableMini').append(template({'cabDetails':data, 'filter':'Mini'}));
            $('#cabDetailsTableSedan').append(template({'cabDetails':data, 'filter': 'Sedan'}));
            console.log(data);
        }
    });
}
