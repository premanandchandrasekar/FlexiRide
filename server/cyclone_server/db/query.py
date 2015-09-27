_INSERT_BOOKED_CAB = \
    'INSERT INTO CabsBooked(driver_name, cab_number,'\
    ' driver_mobile_number, sharing, device_id,'\
    ' estimated_amount, estimated_time VALUES(%s, %s,'\
    ' %s, %s, %s, %s, %s, %s) RETURNING *;'

_INSERT_INTO_USER_DETAILS = \
    'INSERT INTO UserDetails(booking_id, user_mobile_number,'\
    ' pickup_location, destination, estimated_amount) VALUES('\
    ' %s, %s, %s, %s, %s);'

_FETCH_BOOKED_CABS_BY_ID = \
    'SELECT * FROM CabsBooked WHERE id = %s;'

_GET_BOOKED_DETAILS_BY_CRN = \
	'SELECT * FROM CabsBooked WHERE crn = %s;'
