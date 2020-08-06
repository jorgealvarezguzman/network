function createTextarea(id, text) {
    document.getElementById(`${id}`).innerHTML =
    '<textarea id="textarea" maxlength="512" rows="3" style="width:100%;max-width:100%;">' + text + '</textarea>' + '<br>' +
    '<button class="btn btn-primary" onclick="fetchHtml(' + id + ')">Save</button>';
}

function fetchHtml(id) {
    fetch('./{{user.id}}')
    .then(function(response){
        return response.text();
    })
    .then(function(html){
        var content = document.getElementById("textarea").value;
        document.getElementById(id).innerHTML = content;

        fetch('../updatepost', {
          method: 'POST', // or 'PUT'
          body: JSON.stringify({
              post_id: id,
              content: content
          })
        })
        .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }
            }
          )
          .catch(function(err) {
            console.log('Fetch Error :-S', err);
          });
    });
}

function fetchLikes(post_id){
    fetch(`http://127.0.0.1:8000/likepost/${post_id}`)
    .then(function(response){
        return response.text();
    })
    .then(function(html){
        document.body.innerHTML = html;
    })
    .catch(function(err) {
        location.reload();
    });
}
