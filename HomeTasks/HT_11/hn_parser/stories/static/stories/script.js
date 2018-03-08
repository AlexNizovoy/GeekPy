var acc = document.getElementsByClassName("accordion");
    for (var i = 0; i < acc.length; i++) {
        acc[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var panel = this.nextElementSibling;
            if (panel.style.maxHeight){
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
            for (var k = 0; k < acc.length; k++) {
                if ((acc[k] != this) && (acc[k].nextElementSibling.style.maxHeight)) {
                    acc[k].classList.toggle("active")
                    acc[k].nextElementSibling.style.maxHeight = null;
                }
            }
        });
    }

$(document).ready(function() {
    var options = {
        target:        '#status',   // target element(s) to be updated with server response
        // beforeSubmit:  showRequest,  // pre-submit callback
        success:   redirect,  // post-submit callback
        error:     redirect,
        // other available options:
        url:       "/",  // override for form's 'action' attribute
        type:      "post",       // 'get' or 'post', override for form's 'method' attribute
        dataType:  "json",        // 'xml', 'script', or 'json' (expected server response type)
        clearForm: true,        // clear all form fields after successful submit
        resetForm: true        // reset the form after successful submit

        // $.ajax options can be used here too, for example:
        //timeout:   3000
    };

    // bind to the form's submit event
    $('#parse_form').submit(function() {
        // inside event callbacks 'this' is the DOM element so we first
        // wrap it in a jQuery object and then invoke ajaxSubmit
        // disable submit button for prevent requests
        $("#buttonSubmit").prop("disabled", true);
        $(this).ajaxSubmit(options);
        $("#status").css("visibility", "visible");
        url = "/parsing_status?key=" + $("input[name=csrfmiddlewaretoken]").val();
        interval_id = setInterval(progressWorker, 2000, url);
        // !!! Important !!!
        // always return false to prevent standard browser submit and page navigation
        return false;
    });
});

function redirect() {
    console.log("pass");
    window.location.href="/";
}

function progressWorker(url){
    percent = 0;
    $.ajax({
        url: url,
        async: true,
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log(data);
            $("#status").html(data.msg);
        },
        complete: function(){
            console.log("complete");
        },
        error: function (jqXHR, textStatus, errorThrown) {
                      if (jqXHR.status == 500) {
                          alert('Internal error: ' + jqXHR.responseText);
                      } else {
                          alert('Unexpected error.');
                      }
        }
    });
}
