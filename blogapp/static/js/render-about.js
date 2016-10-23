var About = React.createClass({
  render: function() {
    return (
      <div>
        <h1><b>About</b></h1>
        <div className="w3-section w3-bottombar"></div>
        <h2>Bwatt</h2>
        <p>
          {"Jongleur depuis une demi-douzaine d'années, j'ai essayé pas mal de disciplines (balles, baton du diable, bollas) avant de me focaliser sur quelques- unes qui m'ont le plus plu : le staff (contact), les massues, et, depuis peu, le chapeau. "}
        </p>
        <h2>Suze</h2>
        <p>
          {"Jongleuse à mes heures perdues, je suis parfois acharnée, et parfois très faignante, ce qui me permet d'essayer aussi bien les balles et le diabolo que la balle contact. Parfois même je m'essaye à d'aures choses, lorsque le besoin de changement s'en fait ressentir"}
        </p>
      </div>
    );
  }
});

ReactDOM.render(
  <About data={data} />,
  document.getElementById('content')
);
