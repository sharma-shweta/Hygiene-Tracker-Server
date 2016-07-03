from flask import jsonify, make_response

def __OK__():
	message =  {
		'message': 'Success!',
	}
	return make_response(jsonify(message), 200)

def __NOT_FOUND__():
	message = {
		'message': 'Not Found!',
	}
	return make_response(jsonify(message), 404)
