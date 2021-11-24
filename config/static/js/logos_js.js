function message_error(obj){
    var html_tags = '';
    if (typeof (obj) === 'object' ) {
        html_tags = '<ul style="text-align: left;">';
        $.each(obj, function(key, value) {
            html_tags += '<li>' + key + ': ' + value + '</li>';
        });
        html_tags += '</ul>';
    }
    else {
        html_tags = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html_tags,
        icon: 'error'
    });
}

function u2pckg_validate(units){
    html_tags = ''


    units.forEach(function(value, index){

        if (value['package_id'] != null) {
            html_tags += '<ul style="text-align: left;">';
            html_tags += '<li>' + value['code'] + ' ' + value['name'] + '</li>';
            html_tags += '</ul>';
        }
      })
      const swalButtons = Swal.mixin({
        customClass: {
          confirmButton: 'btn btn-outline-success float-right',
          cancelButton: 'btn btn-outline-danger float-left'
        },
        buttonsStyling: false
      })
      swalButtons.fire({
        title: 'Las siguientes unidades ya tienen paquetes asociados, si continúa, pasarán a formar parte del nuevo paquete ',
        html: html_tags,
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Continuar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true,
    }).then((result) => {
        if (result.value) {
            $.ajax({
                type: 'POST',
                url: window.location.pathname,
                data: {
                    'action': 'validate',
                    'unit_ids': unit_ids
                },
            });
        }
    })
}


