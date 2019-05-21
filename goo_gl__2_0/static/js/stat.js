scrollBox = document.getElementsByClassName('stat-container');
scrollBox = scrollBox[0];

var stat_container = document.getElementsByClassName('stat-container')[0];
var server_address = 'http://82.193.112.187:3/r/'
var received_blocks_count = 0
var response_arr


if ( location.pathname == '/stat/' ) {
    user_id = 0
}
else if ( user_id == 0 &&  location.pathname == '/pstat/' ) {
    location.pathname = '/stat/'
}

append_blocks(0,16)

scrollBox.onscroll = function() { 
    if ( scrollBox.scrollTopMax == scrollBox.scrollTop ) { 
        append_blocks(received_blocks_count +1, 16);
    }
}

function append_blocks(start_by, limit, is_sort=true) {
    let xhr = new XMLHttpRequest();
    let params = 'start_by=' + encodeURIComponent(start_by);
    params += '&limit=' + encodeURIComponent(limit);
    params += '&user_id=' + encodeURIComponent(user_id);
    params += '&is_sort=' + encodeURIComponent(is_sort);
    xhr.open("GET", '/g/json?' + params, true);
    xhr.send();
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status != 200) {
            alert( 'Error! ' + xhr.status + ': ' + xhr.statusText );
        } else {
            response_arr = xhr.responseText;
            response_arr = JSON.parse(response_arr)
            if ( response_arr['status']['code'] == 4 ) {
                scrollBox.onscroll = null;
            }
            else if ( response_arr['status']['code'] != 0 ) {
                alert( 'Error! ' + response_arr['status']['code'] + ': ' + response_arr['status']['text'] );
            } else {
                if ( response_arr['items'].length < limit ) {
                    scrollBox.onscroll = null;
                }
                response_arr['items'].forEach(function(item, i) {
                    let redirect = item['redirect']
                    let landing = server_address + item['landing']
                    let views = item['views']
                    
                    let block = "<div class='link-container'>"
                    block += "    <div class='vertical-link-container'>"
                    block += "        <a class='link-stat' href='" + redirect + "'>" + redirect + "</a>"
                    block += "           <a class='link-stat' href='" + landing + "'>" + landing + "</a>"
                    block += "    </div>"
                    block += "    <div class='list-container-space'></div>"
                    block += "    <span class='view-stat-counter'>" + views + "</span>"
                    block += "</div>"
                    stat_container.innerHTML += block
                    received_blocks_count += 1
                });
            }
        }
    }
}
