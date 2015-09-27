from cyclone.web import URLSpec
from cyclone_server import views
from cyclone_server import api


def munge_route_list(rl):
    new_l = []
    for item in rl:
        if isinstance(item, list):
            new_l.extend(munge_route_list(item))
        else:
            new_l.append(item)
    return new_l


routes = munge_route_list([
    URLSpec(r'/', views.IndexHandler),
    URLSpec(r'/api/latest/getdetail', api.DetailsHandler),
    URLSpec(r'/cam', views.SampleWebcamHandler, name="sample_cam"),
    URLSpec(r'/api/latest/camupload', api.CamUploadHandler),
    URLSpec(r'/api/latest/fetch/available/cabs', api.FetchAvailableCabs),
    URLSpec(r'/location', views.SampleLocationHandler, name="sample_loc"),
    URLSpec(r'/api/latest/fetch/available/showconfirmation', views.ShowConfirmationHandler)
    URLSpec(r'/api/latest/cab/booking', api.CabBookingHandler),
    URLSpec(r'/show_bookedcabs_details', views.ShowBookedCabsDetails, name="booked_cabs"),
    URLSpec(r'/api/latest/bookedcabsdetails', api.BookedCabsHandler)


])
