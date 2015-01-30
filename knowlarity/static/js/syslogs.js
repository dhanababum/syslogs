$(document).ready(function(){

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}




    $('#refresh').click(function(){
    
        var date = $('.pgs:last').attr('date');
        $.ajax({
            type:'POST',
            url: '/new_logs/',
            data:{'date': date},
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                        // Send the token to same-origin, relative URLs only.
                        // Send the token only if the method warrants CSRF protection
                        // Using the CSRFToken value acquired earlier
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
            success: function(res){
                if (res.success){
                    $('.pgs').css('background','#fff');
                   var count = $('.pgs').length
                    $.each(res.logs, function(index, obj){
                        if ($('#'+obj['id']).length){
                            $('#'+obj['id']).css('background','orange');
                            $('#'+obj['id']).find('td:eq(3)').text(obj['occured']);
                        }
                        else{
                            count += 1;
                            var str = '<tr class="pgs" date="'+obj["updated_date"]+'" id="'+obj["id"]+'" style="background: orange;">'+
                                '<td>'+count+'</td>'+
                                '<td>'+obj["id"]+'</td>'+
                                '<td>'+obj["programme"]+'</td>'+
                                '<td>'+obj["occured"]+'</td></tr>';
                            $('tbody').append(str);
                        }
                    });
                }
            },
            error: function(){
            //
            },
        });
    });

});
