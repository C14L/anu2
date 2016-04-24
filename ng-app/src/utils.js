
function tr(str, arr){
    /**
     * Return a translation string from TR_LANGUAGE. If str is not found in 
     * TR_LANGUAGE, then return str with {n} values replaced accordingly.
     *
     * str: String to be translated. can include {0}, {1}, ... {n} placeholders
     *      to be substituted by the relative value in the arr Array.
     * arr: optional Array with values that are inserted into the str String at
     *      the position of {n} = arr[n]. If {n} is not found, ignore arr[n], 
     *      and if arr[n] is not found in str, then ignore it, too.
     *
     * Example: tr("H{0}, {1}!", ["ello", "world"]); --> Hello, world!
     *
     */        
    var msgstr = str;
    if (typeof(TR_LANGUAGE) == 'object'){ // find translation
        for (var i=0; i<TR_LANGUAGE.length; i++){
            if (TR_LANGUAGE[i] && TR_LANGUAGE[i]['msgid'] == str){ // found translation!
                msgstr = TR_LANGUAGE[i]['msgstr'];
                break;
    }}};
    if (arr && arr[0]){ // replace untranslatable values
        for (var i=0; i<arr.length; i++){ // since javascript doesn't have global replace for String, do split and join
            if (typeof(arr[i]) == 'string' || typeof(arr[i]) == 'number'){
                msgstr = msgstr.split('{'+i+'}').join(arr[i]);
    }}};
    return msgstr;
}

function urlencode(str){
    return encodeURIComponent(str);
}

function urldecode(str){
    return decodeURIComponent( ( str+'' ).replace( /\+/g, '%20' ) );
}

function set_cookie(name, value, days){
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    // Replace any ";" in value with something else
    value = ('' + value).replace(/;/g, ',');
    document.cookie = urlencode(name) + "=" + urlencode(value) + expires + "; path=/";
}

function get_cookie(name){
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0)
            return urldecode(c.substring(nameEQ.length, c.length));
    }
    return null;
}

function delete_cookie(name){
    setCookie(name, "", -1);
}

function get_time_delta_seconds(ts){
    var now = new Date().getTime() / 1000;
    var ts_time = new Date( ts ).getTime() / 1000;
    return Math.floor( now - ts_time );
}

function get_time_delta(ts){
    var unit = 'seconds ago';
    var dif = get_time_delta_seconds(ts);

    if (dif > 59) { dif /= 60; unit = 'minutes ago';
      if (dif > 59) { dif /= 60; unit = 'hours ago';
        if (dif > 23) { dif /= 24; unit = 'days ago';
          if (dif > 29) { dif /= 30; unit = 'months ago';
            if (dif > 11) { dif /= 12; unit = 'years ago'; 
    } } } } }
    if (dif < 0) dif = 0;
    return Math.floor(dif) + ' ' + unit;
}

function get_pics_urls(pic_id_list){
    // Returns all URLs for a list of pics at once.
    var urls = [];
    for(var i=0; i<pic_id_list.length; i++) urls[i] = get_pic_urls(pic_id_list[i]);
    return urls;
}

function get_pic_urls(pic_id){
    // Returns an dict of pic URLs: { 'id': ID, small': URL, 'medium': URL, 'large': URL }
    // If pic_id was invalid, then URL is a placeholder image URL.
    var placeholder = '/static/placeholder.jpg';
    var pics_per_subdir = 10000;
    var sizes = ["small","medium","large"];
    var szdirs = ["s","m","x"];
    var urls = { "id":pic_id };

    if(!pic_id || pic_id != parseInt(pic_id) || pic_id < 1)
        return { "id":pic_id, "small":placeholder, "medium":placeholder, "large":placeholder };

    for(var i=0; i<sizes.length; i++){
        var size = sizes[i];
        var szdir = szdirs[i];
        var subdir = Math.floor(pic_id / pics_per_subdir);
        urls[size] = window.MEDIA_URL + szdir + '/' + subdir + '/' + pic_id + '.jpg';
    };

    return urls;
}

function get_pic_url(pic_id, size){
    // Return the URL path to a user uploaded picture.
    // If "pic_id" is an Array of picture IDs, then returns a corresponding 
    // Array of picture URLs in the given "size".
    var placeholder = '/static/placeholder.jpg';
    var pics_per_subdir = 10000;
    var sizes = ["small","medium","large"];
    var szdirs = ["s","m","x"];
    var i = sizes.indexOf(size)
    if(!pic_id || pic_id != parseInt(pic_id) || pic_id < 1) return placeholder;
    var szdir = szdirs[i]

    var getUrl = function(n){
        var subdir = Math.floor(n / pics_per_subdir);
        return window.MEDIA_URL + szdir + '/' + subdir + '/' + n + '.jpg';
    }

    if (typeof(pic_id) == 'object') {
        var urls = [];
        for (i = 0; i < pic_id.length; i++) urls[i] = getUrl(pic_id[i]);
    } else {
        urls = getUrl(pic_id);
    }

    return urls;
}

function get_profile_url(username){
    return  window.BASE_URL + 'profile/' + username;
}

function get_city_name_from_crc(crc){
    if (crc == '') return '';
    return crc.split(', ')[0];
}

function get_country_name_from_crc(crc){
    if (crc == '') return '';
    return crc.split(', ')[-1];
}

function get_csrf_token(){
    return get_cookie(window.CSRF_COOKIE_NAME);
}

function getLocalStorageObject(key){
    // Gets a string from localStorage, parses it as JSON, and returns the 
    // resulting object. If the sting is not JSON, throws an error. If the 
    // key does not exist in localStorage, returns null.
    var val = localStorage.getItem(key);
    return (val) ? JSON.parse(val) : null;
}

function setLocalStorageObject(key, val){
    // Gets a key name and a JSON object. Saves the object to localStorage after
    // converting it to a JSON string.
    return localStorage.setItem( key, JSON.stringify( val ) );
}

function log( msg ){
    if( window.LOG == true ){
        try { console.log( msg ) } catch( e ){ }
    }
}

function url_path_join () {
    // Combine a list of strings into a URL string.
    var re1 = /^\s+|\s+$/g;
    var re2 = /\/+/g;
    return Array.prototype.slice.call(arguments).map(function (k) { return String(k).replace(re1, '') }).join('/').replace(re2, '/');
}

// used for confirmed flags, mainly "match" and "friends" mutual flags.
function sort_by_confirmed_filter( a, b ){
    if( a['confirmed'] > b['confirmed'] ) return -1;
    if( a['confirmed'] < b['confirmed'] ) return 1;
    return 0;
}

function sort_by_created_filter( a, b ){
    if( a['created'] > b['created'] ) return -1;
    if( a['created'] < b['created'] ) return 1;
    return 0;
}

function get_index( arr, key, val ){
    // for lists of dicts. finds the dict that has a key with value val, and 
    // returns the dict's index value within the arr list.
    //
    // Example:
    // li = [{ 'id':5,'foo':'bar' },{ 'id':8,'baz':'zab' },{ 'id':2, 'di':'da'}]
    // get_index( li, 'baz', 'zab' )
    // --> 1
    // get_index( li, 'foo', 'bar' )
    // --> 0

    for( var i = 0; i < arr.length; i++ ){
        if( arr[i][key] == val ) return i;
    }
    return null;
}

// Returns the index of the item "sel" in Array "arr", that has the format of
// [ [id, val], [id, val], ..., [id, val] ] where "sel" is one of the "id"s.
// Return (-1) if the "sel" doesn't match any of the "id"s.
function helper_get_data_item_index(arr, sel){
    for(var i=0; i<arr.length; i++) if(arr[i][0]==sel) return i;
    return (-1);
};

function helper_get_data_item(arr, sel){
    return arr[ helper_get_data_item_index(arr, sel) ];
};

function get_latest_created( list ){
    // return the latest "created" value in all items of the list
    var latest = '';

    for( var i = 0; i < list.length; i++ ){
        if( latest < list[i]['created'] ) latest = list[i]['created'];
    }

    return latest;
}

function get_earliest_created( list ){
    // return the oldest "created" value in all items of the list
    var earliest = list[0]['created'];

    for( var i = 0; i < list.length; i++ ){
        if( earliest > list[i]['created'] ) earliest = list[i]['created'];
    }

    return earliest;
}

function complete_user_pnasl( pnasl ){
    // completes a the basic "pnasl" data on one user
    if( pnasl['username'] ) pnasl['profile_url'] = get_profile_url( pnasl['username'] );
    if( pnasl['pic'] ) pnasl['pic_url'] = get_pic_urls( pnasl['pic'] );
    if( pnasl['crc'] ){
        pnasl['city_name'] = pnasl['crc'].split( ',' )[0];
    }
    if( pnasl['gender'] ){
        pnasl['gender_choice'] = get_choice_tr( 'gender_choice', pnasl['gender'] );
        pnasl['gender_short'] = get_choice_tr( 'gender_short', pnasl['gender'] );
        pnasl['gender_choice_symbol'] = get_choice_tr( 'gender_choice_symbol', pnasl['gender'] );
    }
    if( pnasl['last_active'] ){
        var delta_secs = get_time_delta_seconds( pnasl['last_active'] );
        pnasl['last_active_delta'] = get_time_delta( pnasl['last_active'] );
        pnasl['is_online'] = delta_secs < window.ONLINE_SECONDS_SINCE_LAST_ACTIVE;
        pnasl['is_idle'] = !pnasl['is_online'] && delta_secs < window.IDLE_SECONDS_SINCE_LAST_ACTIVE;
        pnasl['is_offline'] = !pnasl['is_online'] && !pnasl['is_idle'];
    }
    return pnasl;
}

function combine_unique_by_id( arr1, arr2 ){
    // takes two lists of Objects (dicts) and combines them, returns an array.
    // both lists' objects need to have an "id" field as primary identifier.
    // any objects with duplicate "id" numbers are not added to the resulting
    // array.

    // some shortcuts
    if ( (!arr1 || arr1.length<1) && (!arr2 || arr2.length<1) ) return [];
    if ( !arr1 || arr1.length<1 ) return unique_by_id( arr2 );
    if ( !arr2 || arr2.length<1 ) return unique_by_id( arr1 );

    // there are really two arrays with items each. make sure both have all
    // unique items themselves.
    arr1 = unique_by_id( arr1 );
    arr2 = unique_by_id( arr2 );

    // loop and add elements from arr2 to arr1. skip if a duplicate is found.
    for( var i2=0; i2<arr2.length; i2++ ){
        var found = false;
        for( var i1=0; i1<arr1.length; i1++ ){
            if( arr1[i1]['id'] == arr2[i2]['id'] ){ found = true; break; }
        }
        if( !found ) arr1.push( arr2[i2] );
    }

    return arr1;
}

function unique_by_id( arr ){
    // gets a list of dicts, and each item is identified by an "id" field.
    // returs a list of items wth unique "id" values.
    var ret = [];
    if( !arr || arr.length<2 ) return arr;

    for( var i=0; i<arr.length; i++ ){
        var found = false;
        for( var j=0; j<ret.length; j++ ){
            if( arr[i]['id'] == ret[j]['id'] ){ found = true; break; }
        }
        if( !found ) ret.push( arr[i] );
    }

    return ret;
}



//////////////////////////////////////////////////////////////////////////////

/* It should do the stuff client side and apply some *very basic* markdown,
but mainly it should auto convert links to youtube videos or imgur pictures 
into clickable inline content, everytime a text (Profile texts, Talk post) 
is rendered. --That's all. */

// define regexps outside the function, so they are only compiles once
RE_HREF_WWW = [ // www.example.com/any/where?da=duh
    new RegExp( '(\\\s|^)(www\.[a-zA-Z0-9-\.]+(?:/\\\w+)?)(\\\s|$)', 'gi' ),
    ' $1http://$2$3 '];
RE_MARKDOWN_STYLE_LINK = [ // [some text to become linked](http://example.com/link.html)
    new RegExp( '\\\[([^\\\]]+)\\\]\\\((https?://[^\\\)]+)\\\)', 'gi' ),
    '<a href="$2" rel="nofollow">$1</a>'];
// Youtube embedding: http://www.youtube.com/watch?v=CFerHmcjNcc&feature=youtu.be
// http://www.youtube.com/watch?v=-tJYN-eG1zk&feature=bf_next&list=MLGxdCwVVULXeY3WC3FHdvLJCD2wPy0lIL&index=3
RE_YOUTUBE_COM_VIDEO = [
    new RegExp( "(\\\s|\\\n|^)https?://www\\\.youtube\\\.com/watch\\\?v=([a-zA-Z0-9_-]+)[^\\\s\\\n$]*", 'gi' ),
    '$1<iframe class="embedded video youtube" src="//www.youtube.com/embed/$2" frameborder="0" allowfullscreen></iframe>'];
// Youtube shortlinks: http://youtu.be/MloBWyjwsgY
RE_YOUTU_BE_VIDEO = [
    new RegExp( '(\\\s|\\\n|^)https?://youtu\\\.be/([a-zA-Z0-9_-]+)[^\\\s]*(\\\s|\\\n|$)', 'gi' ),
    '$1<iframe class="embedded video youtube" src="//www.youtube.com/embed/$2" frameborder="0" allowfullscreen></iframe>$3'];
// Imgur image links: http://i.imgur.com/MloBWyjwsgY.(jpg|gif)
// Load the thumbnail image by adding a "b" at the end of the image name,
// e.g. http://i.imgur.com/xZkwUmP.jpg --> http://i.imgur.com/xZkwUmPb.jpg
// and use a ".jpg" extension for thumbs always.
RE_IMGUR_IMAGE_LINK = [
    new RegExp( "https?://(?:i\\\.)?imgur\\\.com/([a-zA-Z0-9_-]+)[slb]?(?:\\\.jpg|\\\.gif|\\\.png)/?", 'gi' ),
    ' <a href="http://i.imgur.com/\$1.jpg"><img class="embedded image imgur" src="http://i.imgur.com/$1b.jpg" alt=""></a> '];
// Imgur subreddit image links: http://imgur.com/r/wtf/rXbFJD3
RE_IMGUR_SUBREDDIT_LINK = [
    new RegExp( "https?://imgur\\\.com/r/[a-zA-Z0-9_-]+/([a-zA-Z0-9_-]+)/?", 'gi' ),
    ' <a href="http://i.imgur.com/$1.jpg"><img class="embedded image imgur" src="http://i.imgur.com/$1b.jpg" alt=""></a> '];
// photobucket.com : they do some weird anti-embedd redir voodoo, so just ignore them.
// tinypic.com : they do some weird anti-embedd redir voodoo, so just ignore them.
// blogspot.com : http://1.bp.blogspot.com/_idTv-GGWH0M/TJ4HPdvTwyI/AAAAAAAABAs/GgO5nPdeH38/s1600/rosa-azul.jpg

// Generic image file link for any other pics
RE_IMAGE_FILE_LINK = [
    new RegExp( "(\\\s|^)(https?://[a-z0-9\.-]+/[^\\\s\\\"'>]+\.)(jpe?g|gif|png|bmp)(?:\\\s|$)", 'gi' ),
    '$1<a href="$2$3"><img class="embedded image others" src="$2$3" alt=""></a> '];
// All other links, just make them clickable. They have to start at the 
// beginning of the string or with a whitespace, to avoid re-linking stuff in
// <a href="http://...">http://... tags that is already linked.
// https://example.com/some/thing.html?else=here
RE_HREF_HTTP = [
    new RegExp( '(\\\s|^)(https?://\\\S+)(\\\s|$)', 'gi' ),
    '$1<a href="$2" rel="nofollow">$2</a>$3'];
// Remove non-UNIX newline stuffs that Windows or Apple may still add.
RE_FIX_NONSTANDARD_NEWLINES = [ new RegExp( '\\\r', 'g' ), '' ];
// Remove too many (more than 3) newlines in a row.
RE_FIX_TOO_MANY_NEWLINES = [ new RegExp( '\\\n{4,}', 'g' ), '\n\n\n' ];
// newlines into HTML newlines
RE_PARAGRAPH = [ new RegExp( '\\\n', 'g' ), '\n<br>\n' ];

function textfilter( str ){
    if( !str ) return '';
    str = str.replace( '<', '&lt;' ); // convert html tags to 
    str = str.replace( '>', '&gt;' ); // normal text first.
    str = str.replace( RE_FIX_NONSTANDARD_NEWLINES[0], RE_FIX_NONSTANDARD_NEWLINES[1] );
    str = str.replace( RE_FIX_TOO_MANY_NEWLINES[0], RE_FIX_TOO_MANY_NEWLINES[1] );
    str = str.replace( RE_HREF_WWW[0], RE_HREF_WWW[1] ); // www.x.com --> http://www.x.com
    //str = str.replace( RE_USERNAME[0], RE_USERNAME[1] ); // @username --> <a href="...">@username</a>
    //str = str.replace( RE_HASHTAG[0], RE_HASHTAG[1] ); // #hashtag --> <a href="...">#hashtag</a>
    str = str.replace( RE_MARKDOWN_STYLE_LINK[0], RE_MARKDOWN_STYLE_LINK[1] );
    str = str.replace( RE_PARAGRAPH[0], RE_PARAGRAPH[1] );
    str = str.replace( RE_IMGUR_IMAGE_LINK[0], RE_IMGUR_IMAGE_LINK[1] );
    str = str.replace( RE_IMGUR_SUBREDDIT_LINK[0], RE_IMGUR_SUBREDDIT_LINK[1] );
    str = str.replace( RE_YOUTUBE_COM_VIDEO[0], RE_YOUTUBE_COM_VIDEO[1] );
    str = str.replace( RE_YOUTU_BE_VIDEO[0], RE_YOUTU_BE_VIDEO[1] );
    // last
    str = str.replace( RE_HREF_HTTP[0], RE_HREF_HTTP[1] ); // http://www.x.com -> <a href="..."
    return str;
}

//////////////////////////////////////////////////////////////////////////////