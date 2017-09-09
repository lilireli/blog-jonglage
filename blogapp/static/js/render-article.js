var articleComponent = Vue.component('content-page', {
    template: '#template-content-article',
    props: ['page'],
    methods: {
        getDate: function(creationDate, modificationDate) {
            dateString = "le " + creationDate;
            if (creationDate != modificationDate)
            {
                dateString += " (modifié le " +  modificationDate + ")";
            }

            return dateString;
        }
    }
});

var article = new Vue({
    el: "#content",
    data: {
        page: {
            name: "Apprendre le trois balles",
            author: "Suze",
            description: "Un article pour apprendre le trois balles, \u00e9tape par \u00e9tape et avec pleins de conseils annexes pour s'assurer que vous ne serez pas perdus en chemin.",
            url: "apprendre-le-trois-balles",
            category: "Balles",
            page_type: "Balles",
            difficulty: 1,
            creation_date: "12 septembre 2017",
            last_modification_date: "13 septembre 2017",
            tags: [{"name": "convention"}, {"name": "presentation"}],
            content: "<h1>Qu'est ce qu'est une convention de jonglage ?</h1>\n<p>J'ai d\u00e9j\u00e0 fait un article de retour sur la convention de M\u00fcnich, mais il sans pr\u00e9ciser exactement ce qu'\u00e9tait une convention de jonglage. C'est ce que je vais t\u00e2cher de faire ici.\n\u00c0 l'instar de nombreuses disciplines, les jongleurs se retrouvent parfois entre eux dans ce qu'on appelle une convention (comme les conventions de jeux de r\u00f6le). Cependant, c'est un \u00e9v\u00e8nement qui\nressemble \u00e0 peu d'autres \u00e9v\u00e8nements (le seul type que j'ai fait et qui s'en rapproche un tant soit peu au niveau de l'ambiance est le festival de musique). Il s'agit d'un \u00e9v\u00e8nement qui s'\u00e9tale sur un ou\nplusieurs jours (souvent un week-end, et 10 jours pour la convention europ\u00e9enne, l'EJC). On en compte une vingtaine en France (\u00e0 la louche, je n'ai pas compt\u00e9), dont les plus connus sont celles de Rennes, Poitiers, Carvin, Mulhouse, Toulouse (pour la Gl\u00fchwein, la premi\u00e8re de l'ann\u00e9e)... Chaque ann\u00e9e, l'une d'elle est choisit pour \u00eatre la convention Fran\u00e7aise.</p>\n<h1>Que trouve-t-on en convetion ?</h1>\n<p>D'abord, des jongleurs, c'est \u00e9vident. En France, surtout des Fran\u00e7ais, mais toujours quelques \u00e9trangers (surtout pr\u00e8s des fronti\u00e8res). L'\u00e9l\u00e9ment le plus important ensuite est le gymnase (ou parfois les gymnases), un lieu o\u00f9 on trouve toujours des gens en train de jongler, \u00e0 n'importe quelle heure du jour o\u00f9 de la nuit (un ami avait voulu \u00eatre seul dans le gymnase en EJC et \u00e9tait rest\u00e9 tr\u00e8s tard. Malheureusement \u00e7a a \u00e9t\u00e9 impossible. Le temps que les derniers de la nuit partent, les premiers de la journ\u00e9e \u00e9taient arriv\u00e9s). Ensuite un chapiteau (ou une salle) pour les spectacles. Une sc\u00e8ne feu, pour le jongle enflamm\u00e9e, de quoi camper, ou dormir, quelques snacks, et un ou plusieurs marchands de mat\u00e9riel de jonglage (sauf pour les trop petites conventions).\nS'occuper n'est pas le probl\u00e8me, bien au contraire. On arrive en fait rarement tout ce qu'on avait pr\u00e9vu. Une partie de la journ\u00e9e est remplie par des workshops. Des gens proposent en effet de donner des cours sur un truc en particulier. Cela varie \u00e9norm\u00e9ment : des workshops classiques pour maitriser son trois balles, \u00e0 des partages de figures au staff, ou encore le moyen de faire passer une massue derri\u00e8re le dos. Sans oublier les moins classiques : rendez-vous le matin pour une s\u00e9ance de yoga matinal, initiation au go, construction de mat\u00e9riel de jonglage ou origami. Il m'est m\u00eame arriver de faire un \u00e9change de techniques de survie en cas d'attaques zombies ! Comme quoi, il y en a pour tous les go\u00fbts.</p>\n<h1>Spectacles de folies</h1>\n<p>Plusieurs spectacles ponctuent aussi les conventions. Des sc\u00e8nes ouvertes, o\u00f9 chacun peut se produire devant tout le monde. Des spectacles de compagnies de cirque ou de jonglage parfois. Et le tout ponctu\u00e9 par le gala, LE spectacle \u00e0 de pas manquer, constitu\u00e9 de plusieurs num\u00e9ros effectu\u00e9s par des professionnels.\nEnfin, il y a la tente \u00e0 Ren\u00e9gade. Une petite sc\u00e8ne o\u00f9 chacun peut faire un trick (= une figure) original, afin de gagner une bi\u00e8re (ou un shot de Vodka en Pologne...). Le d\u00e9cideur ? Le public, qui, par ses acclamations, va r\u00e9compenser les meilleurs. Attention \u00e0 ne pas faire un petit num\u00e9ro, ou quelque chose qui a d\u00e9j\u00e0 \u00e9t\u00e9 vu et revu en r\u00e9n\u00e9gade (surtout en France, ou le public est particuli\u00e8rement s\u00e9v\u00e8re), ou vous vous ferez taclez et repartirez sans rien. Mais qui ne tente tente rien n'a rien. Des exemples ? Une fois j'ai vu un mec avec un r\u00e9chaud \u00e0 gaz allum\u00e9 sur la t\u00eate se d\u00e9shabiller enti\u00e8rement (et avec un T-shirt, pas une chemise hein). Ou encore un autre attacher une corde \u00e0 un pillier, donner l'autre extr\u00e9mit\u00e9 \u00e0 trois mecs costauds, monter en monocycle sur la corde puis jongler avec trois massues. Ou bien encore un mec lancer son diabolo, faire un saut p\u00e9rilleux en arri\u00e8re, et rattrapper son diabolo apr\u00e8s qu'il ait rebondi sur le sol. Autrement dit, seul votre imagination vous limite. Et comme j'aime \u00e0 le dire, quand je repars de convention, les limites des prouesses humaines ont \u00e9t\u00e9 repouss\u00e9es dans ma t\u00eate.</p>\n<h1>L'ambiance</h1>\n<p>Un dernier mot sur l'ambiance, m\u00eame si il faut la vivre pour la comprendre. Les jongleurs sont gentils, fonci\u00e8rement (enfin, la grande majorit\u00e9). Nonobstant, il est extr\u00eamement facile d'adresser la parole \u00e0 n'importe qui, que ce soit pour discuter ou demander de l'aide sur une figure. Les affaires de chacun sont sur le sol, sans surveillance, et il est possible de prendre n'importe quel mat\u00e9riel pour l'essayer (\u00e0 condition de rester \u00e0 c\u00f4t\u00e9, afin que la personne puisse la r\u00e9cup\u00e9rer quand elle en a envie). Les journ\u00e9es sont ponctu\u00e9es de retrouvailles entre personnes qui se sont vus \u00e0 d'autres conventions. Ce que j'aime le plus, c'est d'\u00eatre l'impression d'\u00eatre dans un autre monde, un mini-microcosme de paix et de libert\u00e9 qui repose du monde ext\u00e9rieur. Et \u00e7a, c'est quelque chose que je n'ai retrouv\u00e9 nulle part ailleurs.</p>"
        }
    }
});
