var categoryComponent = Vue.component('content-page', {
    template: '#template-content-home',
    props: ['page']
});

// create a new Vue instance and mount it to our div element above with the id of app
var vm = new Vue({
    el: '#content',
    data: {
        pagetype: "home",
        page: {
            articles: [
                {
                    name: "Les conventions",
                    creation_date: "29 mars 2017",
                    tags: [
                        {
                            name: "convention"
                        },
                        {
                            name: "presentation"
                        }
                    ],
                    description: "Une pr\u00e9sentation des conventions de jonglage",
                    author: "Bwatt",
                    id: "les-conventions",
                    category: "Journal du jongleur",
                    difficulty: 0
                },
                {
                    name: "Convention M\u00fcnich 2016",
                    creation_date: "24 nov. 2016",
                    tags: [
                        {
                            name: "convention"
                        }
                    ],
                    description: "Un retour sur la convention de M\u00fcnich de 2016",
                    author: "bwatt",
                    id: "convention-munich-2016",
                    category: "Journal du jongleur",
                    difficulty: 0
                },
                {
                    name: "Le quatre balles",
                    creation_date: "14 nov. 2016",
                    tags: [
                        {
                            name: "Quatre Balles"
                        }
                    ],
                    description: "Un article pour apprendre le quatre balles, en passant par l'explication des cascades et fontaines",
                    author: "Suze",
                    id: "le-quatre-balles",
                    category: "Balles",
                    difficulty: 4
                }
            ],
            pagination:
            {
                nb_page: 20,
                current_page: 15
            }
        }
    }
});
