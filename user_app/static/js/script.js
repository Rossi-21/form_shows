// function changeImage(imageId) {
//     var img = document.getElementById(imageId);
//     var favoriteImage = "/static/images/favorite.png";
//     var likedImage = "/static/images/liked.png";

//     if (img.src.includes(favoriteImage)) {
//         img.src = likedImage;
//     } else {
//         img.src = favoriteImage;
//     }
// }

function changeImage(imageId) {
    var img = document.getElementById(imageId);
    if (img.src.includes("/static/images/favorite.png")) {
        img.src = "/static/images/liked.png";
    } else {
        img.src = "/static/images/favorite.png";
    }
}