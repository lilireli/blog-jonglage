var categoryComponent = Vue.component('content-page', {
    template: '#template-content-category',
    props: ['page']
});

var category = new Vue({
    el: "#content",
    data: {
        page: {
            description: "Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage Un des objets les plus basiques au jonglage",
            tags: [
                {
                    articles: [
                        {
                            id: "apprendre-le-trois-balles",
                            difficulty: 1,
                            name: "Apprendre le trois balles",
                            description: "Un article pour apprendre le trois balles, \u00e9tape par \u00e9tape et avec pleins de conseils annexes pour s'assurer que vous ne serez pas perdus en chemin."
                        },
                        {
                            id: "lolilol",
                            difficulty: 1,
                            name: "Lolilol",
                            description: "Un article pour apprendre le trois balles, \u00e9tape par \u00e9tape et avec pleins de conseils annexes pour s'assurer que vous ne serez pas perdus en chemin."
                        }
                    ],
                    name: "Cascade trois balles",
                    description: ""
                },
                {
                    articles: [
                        {
                            id: "apprendre-le-trois-balles",
                            difficulty: 1,
                            name: "Apprendre le trois balles",
                            description: "Un article pour apprendre le trois balles, \u00e9tape par \u00e9tape et avec pleins de conseils annexes pour s'assurer que vous ne serez pas perdus en chemin."
                        },
                        {
                            id: "lolilol",
                            difficulty: 1,
                            name: "Lolilol",
                            description: "Un article pour apprendre le trois balles, \u00e9tape par \u00e9tape et avec pleins de conseils annexes pour s'assurer que vous ne serez pas perdus en chemin."
                        }
                    ],
                    name: "Cascade quatre balles",
                    description: ""
                }
            ],
            page_type: "balles",
            beginner_links: [
                {
                    link: "/articles/apprendre-le-trois-balles",
                    name: "Apprendre le trois balles"
                },
                {
                    link: "/articles/lolilol",
                    name: "Lolilol"
                }
            ],
            name: "Balles"
        }
    }
});
