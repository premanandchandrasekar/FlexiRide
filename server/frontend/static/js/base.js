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

});

