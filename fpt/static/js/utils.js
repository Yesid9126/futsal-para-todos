function likeProduct() {
    let value = document.getElementById('css-stars').value
    if (value) {
        parent_star = document.getElementById('loading')
        parent_star.hidden = false
        element_stars = document.getElementsByClassName('br-widget')[0]
        element_stars.disabled = true
        element_stars.hidden = true
        parent_star.innerHTML = '<i class="fa fa-spinner fa-spin"></i>'
    }
    if (deliveryPK) {
        $.ajax({
            type: "POST",
            url: `/api/contents/${deliveryPK}/rating/`,
            data: {
                'rating': value,
                'id_content': content_pk,
                'csrfmiddlewaretoken': crsf_token,
                'user': userPK
            },
            dataType: "json"
        }).done(function (response) {
            parent_star.hidden = true
            element_stars.disabled = false
            element_stars.hidden = false
            if (response.success) {
                toastr.success(gettext('Gracias por calificar el contenido') + "🌟")
            }
        })
    }
}
