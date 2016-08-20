var Menu = React.createClass({
    close: function() {
        document.getElementById("mySidenav").style.display = "none";
        document.getElementById("myOverlay").style.display = "none";
    },
    render: function() {
        return (
          <div>
            <nav className="w3-sidenav w3-collapse w3-white w3-animate-left w3-padding-top" id="mySidenav">
              <div className="w3-container">
                <a href="#" onClick={this.close} className="w3-hide-large w3-right w3-jumbo w3-padding" title="close menu">
                  <i className="fa fa-remove"></i>
                </a>
                <img src="img_avatar_g2.jpg" className="w3-round"></img>
                <h4 className="w3-padding-0"><b>JONGLAGE</b></h4>
                <p className="w3-text-grey">Un blog pour explorer des millions de possibilités</p>
              </div>
              <a href="index.html"            className="w3-padding {if (this.props.data.pageType == 'home') {'w3-text-teal'}}">HOME</a>
              <a href="journal.html"          className="w3-padding {if (this.props.data.pageType == 'journal-du-jongleur') {'w3-text-teal'}}">JOURNAL DE JONGLEUR</a>
              <a href="acrobatie.html"        className="w3-padding {if (this.props.data.pageType == 'acrobatie') {'w3-text-teal'}}">ACROBATIE</a>
              <a href="balles.html"           className="w3-padding {if (this.props.data.pageType == 'balles') {'w3-text-teal'}}">BALLES</a>
              <a href="balle-contact.html"    className="w3-padding {if (this.props.data.pageType == 'balle-contact') {'w3-text-teal'}}">BALLE CONTACT</a>
              <a href="baton-du-diable.html"  className="w3-padding {if (this.props.data.pageType == 'baton-du-diable') {'w3-text-teal'}}">BATON DU DIABLE</a>
              <a href="bolas.html"            className="w3-padding {if (this.props.data.pageType == 'bolas') {'w3-text-teal'}}">BOLAS</a>
              <a href="chapeau.html"          className="w3-padding {if (this.props.data.pageType == 'home') {'w3-text-teal'}}">CHAPEAU</a>
              <a href="diabolo.html"          className="w3-padding {if (this.props.data.pageType == 'home') {'w3-text-teal'}}">DIABOLO</a>
              <a href="massue.html"           className="w3-padding {if (this.props.data.pageType == 'home') {'w3-text-teal'}}">MASSUE</a>
              <a href="staff.html"            className="w3-padding {if (this.props.data.pageType == 'home') {'w3-text-teal'}}">STAFF</a>
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
            <a href="#"><img src="img_avatar_g2.jpg" className="w3-circle w3-right w3-margin w3-hide-large w3-hover-opacity"></img></a>
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
            <div className="w3-third">
              <p>ABOUT</p>
              <p>Powered by <a href="http://www.w3schools.com/w3css/default.asp" target="_blank">w3.css</a></p>
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
