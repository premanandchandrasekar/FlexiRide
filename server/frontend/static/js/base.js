$(document).ready(function(){
    var params = {'pickup_lat':12.921003, 'pickup_lng':77.620707};
    $.get('/api/latest/fetch/available/cabs', params).error(function(res) {
            console.log(res);
        }).then(function(res){
            console.log(res);
            if(res.success){
                var data = res.data.categories;
                _.each(data, function(d){
                    if(d['distance'] == -1){
                        d['distance'] = 2;
                    }
                    if(d['eta'] == -1){
                        d['eta'] = 2;
                    }
                    $('.tab-content>#' + d['display_name'] + '>p').html('<p>Distance to reach ' + d['distance'] + ' ' + d['distance_unit'] +
                        '</p><br><p>Estimated Time to reach ' + d['eta'] + ' ' + d['time_unit']);
                })
            }
        });

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
        var pan_no = $("#idcard").val();
        if((mob_no.length > 0) && (mob_no.length==10)){
            $("#ps_container").hide();
            $(".pan-text-container").hide();
            $("#webcam").hide();
            $(".or_text").hide();
            $(".pan-title").hide();
        } else if((mob_no.length > 0 && mob_no.length < 10)||mob_no == 0){
            $("#error_msg").text("Enter a valid 10 digit mobile number.").css('color', '#f9aa0b').show().fadeOut(2000);
            return;
        }
        $("html, body").animate({ scrollTop: $('#booking_header').offset().top }, 1000);
    });

    $("#pan_go").click(function(e){
        var pan_no = $("#idcard").val();
        if(pan_no.length > 0){
            $("#ps_container").show();
            $("#search_key").hide();
            $("#search_button").hide();
            $(".or_text").hide();
            $(".qt_text").hide();
        } else if(pan_no.length == 0){
            $("#pan_error_msg").text("Enter a valid pan number number.").css('color', '#f9aa0b').show().fadeOut(2000);
            return;
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
  var latitude = place.geometry.location.lat();
  var longitude = place.geometry.location.lng();
  document.getElementById('destination').setAttribute('data-lat', latitude);
  document.getElementById('destination').setAttribute('data-long', longitude);
}
//[End google places autocpmplete]
