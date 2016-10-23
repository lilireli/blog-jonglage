var Menu = React.createClass({
    close: function() {
        document.getElementById("mySidenav").style.display = "none";
        document.getElementById("myOverlay").style.display = "none";
    },
    render: function() {
        var typePage = this.props.data.page_type;
        return (
          <div>
            <nav className="w3-sidenav w3-collapse w3-white w3-animate-left w3-padding-top" id="mySidenav">
              <div className="w3-container">
                <a href="/categories/#" onClick={this.close} className="w3-hide-large w3-right w3-jumbo w3-padding" title="close menu">
                  <i className="fa fa-remove"></i>
                </a>
                <img src="/static/img/img_menu.JPG" className="w3-round"></img>
                <h4 className="w3-padding-0"><b>JONGLAGE</b></h4>
                <p className="w3-text-grey">Un blog pour explorer des millions de possibilités</p>
              </div>
              <a href="/"                            className={"w3-padding " + ((typePage == 'home') ? "w3-text-teal" : "")} >HOME</a>
              <a href="/categories/journal"          className={"w3-padding " + ((typePage == 'journal') ? "w3-text-teal" : "")}>JOURNAL DE JONGLEUR</a>
              <a href="/categories/acrobatie"        className={"w3-padding " + ((typePage == 'acrobatie') ? "w3-text-teal" : "")}>ACROBATIE</a>
              <a href="/categories/balles"           className={"w3-padding " + ((typePage == 'balles') ? "w3-text-teal" : "")}>BALLES</a>
              <a href="/categories/balle-contact"    className={"w3-padding " + ((typePage == 'balle-contact') ? "w3-text-teal" : "")}>BALLE CONTACT</a>
              <a href="/categories/baton-du-diable"  className={"w3-padding " + ((typePage == 'baton-du-diable') ? "w3-text-teal" : "")}>BATON DU DIABLE</a>
              <a href="/categories/bolas"            className={"w3-padding " + ((typePage == 'bolas') ? "w3-text-teal" : "")}>BOLAS</a>
              <a href="/categories/chapeau"          className={"w3-padding " + ((typePage == 'chapeau') ? "w3-text-teal" : "")}>CHAPEAU</a>
              <a href="/categories/diabolo"          className={"w3-padding " + ((typePage == 'diabolo') ? "w3-text-teal" : "")}>DIABOLO</a>
              <a href="/categories/massue"           className={"w3-padding " + ((typePage == 'massue') ? "w3-text-teal" : "")}>MASSUE</a>
              <a href="/categories/staff"            className={"w3-padding " + ((typePage == 'staff') ? "w3-text-teal" : "")}>STAFF</a>
            </nav>

            { /* Overlay effect when opening sidenav on small screens */ }
            <div className="w3-overlay w3-hide-large w3-animate-opacity" onClick={this.close} title="close side menu" id="myOverlay"></div>
          </div>
        );
    }
});

var MenuMobile = React.createClass({
    open: function() {
        document.getElementById("mySidenav").style.display = "block";
        document.getElementById("myOverlay").style.display = "block";
    },
    render: function() {
        return (
          <header className="w3-container">
            <a href="/categories/#"><img src="img_avatar_g2.jpg" className="w3-circle w3-right w3-margin w3-hide-large w3-hover-opacity"></img></a>
            <span className="w3-opennav w3-hide-large w3-xxlarge w3-hover-text-grey" onClick={this.open}><i className="fa fa-bars"></i></span>
          </header>
        )
    }
});

var Footer = React.createClass({
    render: function() {
        return (
          <footer className="w3-container w3-padding-32 w3-white">
          <div className="w3-row-padding">
            <div className="w3-quarter">
              <p>ABOUT</p>
              <p>Nous contacter : {'jonglage<at>bwatt.eu'}</p>
            </div>

            <div className="w3-half w3-center">
              <p>
                Powered by <a href="http://www.w3schools.com/w3css/default.asp" target="_blank">w3.css</a>, <a href="https://facebook.github.io/react/" target="_blank">React</a>, <a href="http://flask.pocoo.org/" target="_blank">Flask</a> and <a href="https://mariadb.org/" target="_blank">MariaDB</a>
                <br/>
                Engineered with <a href="https://github.com/lilireli/blog-jonglage" target="_blank">a Github project</a>
              </p>
            </div>

            <div className="w3-quarter">
              <p>
                <a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/fr/">
                  <img alt="Licence Creative Commons" className="licence w3-display-right" src="https://i.creativecommons.org/l/by-nc/3.0/fr/88x31.png" />
                </a>
              </p>
            </div>
          </div>
          </footer>
        )
    }
})

ReactDOM.render(
  <Menu data={data} />,
  document.getElementById('nav-container')
);

ReactDOM.render(
  <MenuMobile />,
  document.getElementById('nav-container-mobile')
);

ReactDOM.render(
  <Footer />,
  document.getElementById('footer')
)
