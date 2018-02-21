$(document).ready(function() {
    // make accordion switch
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

    // AjaxSubmit for update stories
    var options = {
        target:        '#status',   // target element(s) to be updated with server response
        beforeSubmit:  start_check_status,  // pre-submit callback
        success:   redirect_succ,  // post-submit callback
        complete:  redirect_compl,
        error:     redirect_err,
        // other available options:
        // url:       "/",  // override for form's 'action' attribute
        // type:      "post",       // 'get' or 'post', override for form's 'method' attribute
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

        // !!! Important !!!
        // always return false to prevent standard browser submit and page navigation
        return false;
    });

//    Make active current nav-element
    var a_set = $('ul.nav>li a');
    if (a_set.length) {
        for (var i = 0; i < a_set.length; i++) {
            if (a_set[i].href === window.location.href) {
                a_set[i].parentElement.classList.add('active');
            }
        }
    }

});

function redirect_succ(data) {
    window.location.href="/" + "?succ=True";

}

function redirect_compl(data) {
    window.location.href="/" + "?compl=True";

}

function redirect_err(data) {
    window.location.href="/" + "?err=True";

}

function start_check_status(data) {
    var url = "/parser/status?key=" + $("input[name=csrfmiddlewaretoken]").val();
    var interval_id = setInterval(progressWorker, 3000, url);
}

function progressWorker(url){
    $.ajax({
        url: url,
        async: true,
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            $("#status").html(data.msg);
            if (data.complete === true) {
                redirect();
            }
        },

        error: function (jqXHR, textStatus, errorThrown) {
                      if (jqXHR.status === 500) {
                          alert('Internal error: ' + jqXHR.responseText);
                      } else {
                          alert('Unexpected error.');
                      }
        }
    });
}
