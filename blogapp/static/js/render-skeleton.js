var menu = new Vue({
    el: "#nav-container",
    data: {
        categories: [
            { name: "Balles", id: "balles" },
            { name: "Staff", id: "staff" }
        ],
        page_type: "balles"
    },
    methods: {
        classActivated: function(catPage, catNav) {
            return catPage == catNav;
        },
        closeMenu: function() {
            document.getElementById("mySidenav").style.display = "none";
            document.getElementById("myOverlay").style.display = "none";
        }
    }
});

var menuMobile = new Vue({
    el: '#nav-container-mobile',
    methods: {
        openMenu: function () {
            document.getElementById("mySidenav").style.display = "block";
            document.getElementById("myOverlay").style.display = "block";
        }
    }
});

var articleListByTag = Vue.component('list-article-by-tag', {
    template: '#template-list-article-by-tag',
    props: ['page'],
    methods: {
        handleClickTag: function(tag) {
            /* Open and close the accordion */
            var x = document.getElementById(tag);
            if (x.className.indexOf("w3-show") == -1) {
                x.className += " w3-show";
            } else {
                x.className = x.className.replace(" w3-show", "");
            }
        },
        handleClickArticle: function(article) {
            window.location = "/articles/" + article;
        }
    }
})

var articleListByTimeline = Vue.component('list-article-by-timeline', {
    template: '#template-list-article-by-timeline',
    props: ['page'],
    methods: {
        handleClickArticle: function(article) {
            window.location = "/articles/" + article;
        },
        paginate: function(iteratedPage, currentPage, maxPage){
            var className = "w3-hover-black";
            if (iteratedPage == currentPage){ className = "w3-black"; }

            var link = '<a class='+className+' href=/page/'+iteratedPage+'>'+iteratedPage+'</a>';

            /* Do not render all pages number but Page 1 and last page are always rendered */
            if (iteratedPage != 1 && iteratedPage != maxPage){
                /* Small page numbers */
                if (currentPage > 5){
                    var linkSmaller = '<a class="w3-hover-black" href=/page/'+iteratedPage+'>«</a>';

                    if (currentPage > maxPage - 3){
                        if (iteratedPage == maxPage - 5){ link = linkSmaller; /* Insert << */ }
                        else if (iteratedPage < maxPage - 5 ){ link = ''; /* Number is too small */ }
                    }
                    else {
                        if (iteratedPage == currentPage - 3){ link = linkSmaller; /* Insert << */ }
                        else if (iteratedPage < currentPage - 3 ){ link = ''; /* Number is too small */ }
                    }
                }

                /* Big page numbers */
                if (currentPage < maxPage - 4){
                    var linkBigger = '<a class="w3-hover-black" href=/page/'+iteratedPage+'>»</a>';

                    if (currentPage < 4){
                        if (iteratedPage == 6){ link = linkBigger; /* Insert >> */ }
                        else if (iteratedPage > 6){ link = ''; /* Number is too big */ }
                    }
                    else {
                        if (iteratedPage == currentPage + 3){ link = linkBigger; /* Insert >> */ }
                        else if (iteratedPage > currentPage + 3){ link = ''; /* Number is too big */ }
                    }
                }
            }

            return link;
        }
    }
})
