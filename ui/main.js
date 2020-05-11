function formHoldOn() {
    HoldOn.open({
        theme: "sk-cube-grid"
    });
}

function closeHoldOn() {
    HoldOn.close();
}

function displaySweetalert(title, text, type) {
    swal({
        title: title,
        text: text,
        type: type
    });

}
function displaySweetalertWithOk(title,text,type,modal_id) {
    swal({
        title: title,
        text: text,
        type: type
    },function(){
        $('#'+modal_id).modal('hide');
    });

}

function searchImage() {
    var search_input = $('#search_input').val();
    if (trimText(search_input) !== "") {

        $('#search_results').hide();
        var url =base_url+"/query_images";
        var data = {'query': search_input,'k':10};
        formHoldOn();
        guzzleCallAjax(url, data, 'GET').then(function (response) {
            if (response[0]) {
                var image_list = response[1];
                if (image_list.length === 0) {
                    displaySweetalert('Error', 'No image found!!!', 'error');
                } else {
                    displayImages(image_list, search_input);
                }
            } else {
                displaySweetalert('Error', response[1], 'error');
            }
            closeHoldOn();
        }).catch(function (err) {
            displaySweetalert('Error', err,'error');
            closeHoldOn();
        });
    } else {
        displaySweetalert('Error', 'Kindly add some text to search images!!!', 'error');
    }

}

function changeInputFormat(id) {
    var text = $('#'+id).val();
    text = text.replace(/\s+/g, ' ');
    if (text.length > 0) {
        if (text[0] === " ") {
            text = text.replace(text[0], '');
        }
    }
    $('#'+id).val(text);
}
function trimText(text)
{
    return text.replace(/&nbsp;|<\/?[^>]+(>|$)/g, "").trim();
}

function displayImages(images, search_text) {
    var html = "";
    for (var i = 0; i < images.length; i++) {
        var image_url = base_url+"/serve_image?image="+images[i]['image'];
        html += "<div class='col-sm-3' style='padding: 5px;'>" +
            "<img src='" + image_url + "' alt='" + images[i]['image'] + "' width='250' height='250' title='Score: " + images[i]['score'] + "'>" +
            "</div>"
    }
    $('#search_results_body').html(html);
    $('#search_results_panel_heading').html(search_text.toUpperCase() + " RESULTS");
    $('#search_results').show();
}
var valid_file_extensions = [".jpg", ".png", ".jpeg", ".gif", ".bmp"];
function ValidateSingleInput(image) {
    if (image.type === "file") {
        var file_name = image.files[0].name;
        var file_extension = "."+file_name.split('.').pop().toLowerCase();
        if (file_name.length > 0) {
            if($.inArray(file_extension,valid_file_extensions) === -1)
            {
                displaySweetalert("Error","Sorry, " + file_name + " is invalid, allowed extensions are: " + valid_file_extensions.join(", "),'error');
                image.value = "";
            }
        }
    }
}
function validateSaveImageFormData() {
    if($('#image')[0].files.length === 0)
    {
        displaySweetalert("Error","Please select an image first.","error");
    }
    else if(trimText($('#image_description').val()) === "")
    {
        displaySweetalert("Error","Please add image description first.","error");
    }
    else
    {
        // $('#add_image_form').attr('action',base_url+"/add_record");
        // $('#add_image_form').submit();
        var url =base_url+"/add_record";
        var data = new FormData($('#add_image_form')[0]);
        formHoldOn();
        guzzleCallAjaxFormData(url, data, 'POST').then(function (response) {
            if (response[0]) {
                if(response[1]['code'] === 1)
                {
                    displaySweetalertWithOk('Success',response[1]['message'] , 'success','modal-add-image');
                }
                else
                {
                    displaySweetalert('Error',response[1]['message'] , 'error');
                }
            } else {
                displaySweetalert('Error', response[1], 'error');
            }
            closeHoldOn();
        }).catch(function (err) {
            displaySweetalert('Error', err,'error');
            closeHoldOn();
        });
    }
}