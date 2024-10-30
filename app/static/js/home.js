function callback(json) {
    var element = document.getElementById('like' + json.id);
    element.textContent = json.like;
}

function like(article_id) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if ((req.readyState == 4) && (req.status == 200)) {
            var json = JSON.parse(req.responseText);
            callback(json)
        }
    }
    req.open('GET', '/api/articles/' + article_id + '/like');
    req.send(null);
}