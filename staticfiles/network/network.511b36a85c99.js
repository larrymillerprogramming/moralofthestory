function Like(postId) {
    let likeId = document.getElementById("likeIdForPost" + postId).innerHTML.trim();

    // If like object exists
    if (likeId != "") {
        fetch('/alllikes/' + likeId)
            .then(response => response.json())
            .then(like => {
            // Print like to console
            console.log(like);
            // If like is currently active, unlike
            if (like.is_liked == true) {
                document.getElementById("likebutton" + postId).classList.remove("bi-heart-fill");
                document.getElementById("likebutton" + postId).classList.add("bi-heart");
                // Update like count
                let currentCount = document.getElementById("likecounter" + postId).innerHTML;
                let newCount = parseInt(currentCount) - 1;
                document.getElementById("likecounter" + postId).innerHTML = newCount
                fetch('/alllikes/' + likeId, {
                    method: 'PUT',
                    body: JSON.stringify({
                        is_liked: false
                    })
                })
            }
            // If like is currently inactive, like
            else {
                document.getElementById("likebutton" + postId).classList.remove("bi-heart");
                document.getElementById("likebutton" + postId).classList.add("bi-heart-fill");
                // Update like count
                let currentCount = document.getElementById("likecounter" + postId).innerHTML;
                let newCount = parseInt(currentCount) + 1;
                document.getElementById("likecounter" + postId).innerHTML = newCount
                fetch('/alllikes/' + likeId, {
                    method: 'PUT',
                    body: JSON.stringify({
                        is_liked: true
                    })
                })
            }
        });
    } 
    // If like object does not exist yet, create one
    else {
        document.getElementById("likebutton" + postId).classList.remove("bi-heart");
        document.getElementById("likebutton" + postId).classList.add("bi-heart-fill");
        // Update like count
        let currentCount = document.getElementById("likecounter" + postId).innerHTML;
        let newCount = parseInt(currentCount) + 1;
        document.getElementById("likecounter" + postId).innerHTML = newCount
        const liker = document.querySelector('#profileLink').innerHTML;
        // Add like object to API
        fetch('/alllikes', {
            method: 'POST',
            body: JSON.stringify({
                liker: liker,
                postId: postId
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            let objid = result[result.length - 1].id
            console.log(objid);
            document.getElementById("likeIdForPost" + postId).innerHTML = objid;
        });
    }
}

function Follow(username) {
    console.log(username);
    let followId = document.getElementById("followIdForAccount" + username).innerHTML.trim();

    // If follow object exists
    if (followId != "") {
        fetch('/follows/' + followId)
            .then(response => response.json())
            .then(follow => {
            // Print follow to console
            console.log(follow);
            // If follow is currently active, unfollow
            if (follow.is_following == true) {
                document.getElementById("followbutton" + username).innerHTML = "Follow";
                // Update follow count
                let currentCount = document.getElementById("followercounter" + username).innerHTML;
                let newCount = parseInt(currentCount) - 1;
                document.getElementById("followercounter" + username).innerHTML = newCount
                fetch('/follows/' + followId, {
                    method: 'PUT',
                    body: JSON.stringify({
                        is_following: false
                    })
                })
            }
            // If follow is currently inactive, follow
            else {
                document.getElementById("followbutton" + username).innerHTML = "Unfollow";
                // Update follow count
                let currentCount = document.getElementById("followercounter" + username).innerHTML;
                let newCount = parseInt(currentCount) + 1;
                document.getElementById("followercounter" + username).innerHTML = newCount
                fetch('/follows/' + followId, {
                    method: 'PUT',
                    body: JSON.stringify({
                        is_following: true
                    })
                })
            }
        });
    } 
    // If follow object does not exist yet, create one
    else {
        document.getElementById("followbutton" + username).innerHTML = "Unfollow";
        // Update follow count
        let currentCount = document.getElementById("followercounter" + username).innerHTML;
        let newCount = parseInt(currentCount) + 1;
        document.getElementById("followercounter" + username).innerHTML = newCount
        const currentUser = document.querySelector('#profileLink').innerHTML;
        // Add follow object to API
        fetch('/follows', {
            method: 'POST',
            body: JSON.stringify({
                follower: currentUser,
                account: username
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            let objid = result[result.length - 1].id
            console.log(objid);
            document.getElementById("followIdForAccount" + username).innerHTML = objid;
        });
    }
}

function EditForm(post) {
    let contentdisplay = document.getElementById("postcontent" + post).style.display;
    let formdisplay = document.getElementById("editform" + post).style.display;
    let switchvariable = contentdisplay;
    contentdisplay = formdisplay;
    formdisplay = switchvariable;
    document.getElementById("editform" + post).style.display = formdisplay;
    document.getElementById("postcontent" + post).style.display = contentdisplay;    
}

function SaveEdit(post) {
    console.log(post);
    let newContent = document.getElementById("editcontent" + post).value;
    // Hide edit form and show post with new content
    document.getElementById("postcontent" + post).innerHTML = newContent;
    document.getElementById("editform" + post).style.display = "none";
    document.getElementById("postcontent" + post).style.display = "block";
    // Update post content in API 
    fetch('/postsapi/' + post, {
        method: 'PUT',
        body: JSON.stringify({
            content: newContent
        })
    })
}