$(document).ready(function() {
    $('#content').click(function (e) {
        if (e.target.dataset.action === 'add-to-cart') {
            var form = $('#add-to-cart');
            var productId = e.target.dataset.productId;
            form.children('[name$=product_id]').val(productId);
            $.ajax({
                url: form.attr('action'),
                type: form.attr('method'),
                data: form.serialize(),
                beforeSend: function () {
                    $(e.target).attr('disabled', true)
                },
                success: function (data) {
                    showModal(data['success']);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                      if (jqXHR.status === 500) {
                          showModal(jqXHR.responseText);
                      } else {
                          console.log('Unexpected error. ', jqXHR.responseText);
                      }
                }
            });
            e.preventDefault()
            }
        }
    )
});

function showModal(innerHtml) {
    $('#modal-content').text(innerHtml);
    var modal =$('#modal');
    modal.modal('show');
    setTimeout(function(){modal.modal('hide')}, 1000);
}
