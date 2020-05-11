function callAjax(url, data, type) {
    var response = [];
    $.ajax({
        url: url,
        data: data,
        type: type,
        async: false,

        headers: {
            //'Content-Type': 'multipart/form-data'
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

function guzzleCallAjax(url, data, type) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: type,
            data: data,
            async: true,
        success: function (responseData, status, jqXHR) {
            if (jqXHR.getResponseHeader('content-type').indexOf('text/html') >= 0) {
                var message = "Something went wrong";
                var ele = $(responseData).find('#error-head');
                // console.log(ele);
                if (ele != undefined) {
                    message = ele.html();
                }
                showMessage('error', message);
                resolve([false, message]);
            } else {
                resolve([true, responseData]);
            }
        }
    ,
        error: function (jqXHR, error, errorThrown) {
            if (jqXHR.status === 524) {
                reject("Server request timeout");
            } else if (jqXHR.responseJSON) {
                displayExceptionMessages(jqXHR.responseJSON);
            } else if (errorThrown !== "") {
                reject(errorThrown);
            } else {
                reject("Something went wrong!!");
            }
            closeHoldOn();
        }
    })
        ;

    });

}
function guzzleCallAjaxFormData(url, data, type) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: type,
            data: data,
            async: true,
            processData: false,
            contentType:false,
            success: function (responseData, status, jqXHR) {
                if (jqXHR.getResponseHeader('content-type').indexOf('text/html') >= 0) {
                    var message = "Something went wrong";
                    var ele = $(responseData).find('#error-head');
                    // console.log(ele);
                    if (ele != undefined) {
                        message = ele.html();
                    }
                    showMessage('error', message);
                    resolve([false, message]);
                } else {
                    resolve([true, responseData]);
                }
            }
            ,
            error: function (jqXHR, error, errorThrown) {
                if (jqXHR.status === 524) {
                    reject("Server request timeout");
                } else if (jqXHR.responseJSON) {
                    displayExceptionMessages(jqXHR.responseJSON);
                } else if (errorThrown !== "") {
                    reject(errorThrown);
                } else {
                    reject("Something went wrong!!");
                }
                closeHoldOn();
            }
        })
        ;

    });

}