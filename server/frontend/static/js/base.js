$(document).ready(function(){
    var params = {'pickup_lat':12.97189, 'pickup_lng':77.64115};
    $.get('/api/latest/fetch/available/cabs', params).error(function(res) {
            console.log(res);
        }).then(function(res){
            console.log(res);
        });

    jQuery('.tabs .tab-links a').on('click', function(e)  {
        var currentAttrValue = jQuery(this).attr('href');
 
        // Show/Hide Tabs
        jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
 
        // Change/remove current tab to active
        jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
 
        e.preventDefault();
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
