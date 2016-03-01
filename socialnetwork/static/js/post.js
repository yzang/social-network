/**
 * Created by Yiming on 2/25/2016.
 */

$(function () {
    var lastUpdate = new Date().getTime()
    function getPostlist() {
        $.ajax({
            url: '/socialnetwork/getPostAfter?date=' + lastUpdate,
            method: 'get',
            success: function (result) {
                if (result == null || result.length <= 0) {
                    return;
                }
                console.log(result)
                var innerHtml = $('.timeline').html()
                for (var i = 0; i < result.length; i++) {
                    var content = result[i]["content"]
                    var post_date = result[i]["date"]
                    var avatar = result[i]["image"]
                    var first_name = result[i]["first_name"]
                    var last_name = result[i]["last_name"]
                    var owner_id = result[i]["owner_id"]
                    var profile_url = '/socialnetwork/profile/' + owner_id
                    var appendHtml = '<li class="timeline-indigo"><img class="timeline-icon" src="' + avatar + '"> <div class="timeline-body"> ' +
                        '<div class="timeline-header"> <span class="author">Posted by<a href="' + profile_url + '"> ' + first_name + ' ' + last_name + '</a></span> <span class="date">' + post_date + '</span>' +
                        '</div><div class="timeline-content"> <p>' + content + '</p></div></li>'
                    innerHtml = appendHtml + innerHtml;
                    $('.timeline').html(innerHtml)
                }
                lastUpdate = new Date().getTime()
            }
        })
    }

    $('.reply-btn').click(function () {
        var postId = $(this).attr('id');
        var id=postId.substring(postId.lastIndexOf("-")+1);
        var input = $('.input-' + postId)
        var csrf=getCSRFToken()
        if (input.val().trim().length > 0) {
            //ajax call
            $.ajax({
                url: '/socialnetwork/addReply',
                method: 'post',
                data: {'content': input.val(),'csrfmiddlewaretoken':csrf,'post_id':id},
                success: function (result) {
                    if(result.length>0){
                        var replyPanel = $('.panel-' + postId)
                        var html=""
                        for(var i=0;i<result.length;i++){
                            var content = result[i]["content"]
                            var post_date = result[i]["date"]
                            var avatar = result[i]["image"]
                            var first_name = result[i]["first_name"]
                            var last_name = result[i]["last_name"]
                            var owner_id = result[i]["owner_id"]
                            var profile_url = '/socialnetwork/profile/' + owner_id
                            html += '<div class="chat-message chat-primary"> <div class="chat-contact"> ' +
                                '<img class="reply-avatar" src="'+avatar+'"> ' +
                                '</div><div class="chat-text"><span class="author">' +
                                '<a style="color:white;font-weight: bold;" href="'+profile_url+'">' +first_name+' '+last_name+ '</a></span> ' +
                                '<span class="date">'+post_date+'</span> <div>'+content+'</div> </div> </div>'
                            replyPanel.html(html);
                        }
                        input.val("")
                    }
                }
            })
        }
    });

    function getCSRFToken() {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            if (cookies[i].startsWith("csrftoken=")) {
                return cookies[i].substring("csrftoken=".length, cookies[i].length);
            }
        }
        return "unknown";
    }

    setInterval(getPostlist, 5000);

})
