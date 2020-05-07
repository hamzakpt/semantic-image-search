function callAjax(url, data, type) {
    var response = [];
    $.ajax({
        url: url,
        data: data,
type:type,
async:false,
	crossDomain: true,
        headers: {
            'Content-Type': 'multipart/form-data'
 },
        beforeSend: function (xhr) {

        },
        success: function (responseData, status, jqXHR) {


            if (jqXHR.getResponseHeader('content-type').indexOf('text/html') >= 0) {
                var message = "Something went wrong";
                var ele = $(responseData).find('#error-head');
                if (ele != undefined) {
                    message = ele.html();
                }
                response = [false, message];
displaySweetalert('Error', message, 'error');
                if (message === undefined)
                    message = "Request format is not correct";
            } else {
                response = [true, responseData];
            }
        },
        error: function (jqXHR, error, errorThrown) {
            if (jqXHR.status === 524) {
                response = [false, "Server request timeout"];
            } else if (errorThrown !== "") {
                response = [false, errorThrown];
            } else {
                response = [false, "Something went wrong!!"];
            }
        }
    });

    return response;

}