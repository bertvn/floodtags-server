/**
 * Created by Bert on 11/05/2016.
 */

if (!!window.EventSource) {
    var source = new EventSource('get_data');
} else {
    // Result to xhr polling :(
    console.log("internet explorer?")
}
source.addEventListener('message', function (e) {
    print_tweets(e.data)
}, false);

var print_tweets = function (data) {
    console.log(data);
    data = JSON.parse(data)
    clusters = data.clusters
    var i = 1;
    clusters.forEach(function (cluster) {
        document.getElementById("title" + i).innerHTML = cluster.lcs
        document.getElementById("cluster" + i).innerHTML = "";
        (function (i) {
            cluster.tweets.forEach(function (tweet) {
                $.ajax({
                    dataType: "jsonp",
                    url: "https://api.twitter.com/1/statuses/oembed.json?url=https://twitter.com/" + tweet.username + "/status/" + tweet.id + "&hide_media=false?callback=a",
                    data: null,
                    success: function (data) {
                        document.getElementById("cluster" + i).insertAdjacentHTML("beforeend", data.html);
                        twttr.widgets.load()
                    }
                });
            });
        })(i);
        i++;
    });
    news = data.news
    document.getElementById("news").innerHTML = ""
    news.forEach(function (tweet) {
        console.log(tweet)
        $.ajax({
            dataType: "jsonp",
            url: "https://api.twitter.com/1/statuses/oembed.json?url=https://twitter.com/" + tweet.username + "/status/" + tweet.id + "&hide_media=false?callback=a",
            data: null,
            success: function (data) {
                document.getElementById("news").insertAdjacentHTML("beforeend", data.html);
                twttr.widgets.load()
            }
        });
    });
    locations = data.locations
    locations.forEach(function (location) {
        codeAddress(location)
        //ownAddress(location)
        console.log(location)
    });

};

function toggle(id, button) {
    if (document.getElementById(id).style.display == 'block') {
        $('#' + id).slideUp() //document.getElementById(id).style.display = 'none'
        button.style.backgroundImage = 'url("../static/up.png")'
    } else {
        $('#' + id).slideDown()
        //document.getElementById(id).style.display = 'block'
        button.style.backgroundImage = 'url("../static/down.png")'
    }
}



