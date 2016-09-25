var ArticleSmall = React.createClass({
  handleClick: function() {
    window.location = this.props.data.id;
  },
  render: function() {
    return (
      <div className="w3-container w3-col s3 w3-padding">
        <div className="w3-container w3-pale-blue article-small" onClick={this.handleClick}>
          <h2>{this.props.data.name}</h2>
          <p>{this.props.data.description}</p>
        </div>
      </div>
    );
  }
});


var ArticleSmallList = React.createClass({
  render: function() {
    var articleNodes = this.props.data.map(function(article) {
      return (
        <ArticleSmall data={article} key={article.id} />
      );
    });
    return (
      <div>
        {articleNodes}
      </div>
    );
  }
});

var Tag = React.createClass({
  handleClick: function() {
    /* Open and close the accordion */
    var x = document.getElementById(this.props.data.name);
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else {
        x.className = x.className.replace(" w3-show", "");
    }
  },
  render: function() {
    return (
      <div>
        <button onClick={this.handleClick} className="w3-btn-block w3-left-align">
         {this.props.data.name}
        </button>
        <div id={this.props.data.name} className="w3-accordion-content w3-container w3-white w3-padding-bottom">
          <p>{this.props.data.description}</p>
          <ArticleSmallList data={this.props.data.articles} />
        </div>
      </div>
    )
  }
});

var TagList = React.createClass({
  render: function() {
    var tagNodes = this.props.data.map(function(tag) {
      return (
        <Tag data={tag} key={tag.name} />
      );
    });
    return (
      <div>
        {tagNodes}
      </div>
    );
  }
});

var Links = React.createClass({
  render: function() {
    var linkNodes = this.props.data.map(function(link) {
      return (
        <a href={link.link} className="margin-small-right">{link.name}</a>
      );
    });
    return (
      <span>
        {linkNodes}
      </span>
    );
  }
});

var Category = React.createClass({
  render: function() {
    return (
      <div>
        <h1><b>{this.props.data.name}</b></h1>
        <div className="w3-section w3-bottombar"></div>

        <div className="w3-container w3-margin-bottom">
          <div dangerouslySetInnerHTML={{__html: this.props.data.description}}></div>
        </div>

        <div className="w3-container w3-margin-bottom">
          <h2>Pour bien commencer :</h2>
          Quelques liens : <Links data={this.props.data.beginner_links} />
        </div>

        <div className="w3-container">
          <h2>Voir toutes les figures par catégories :</h2>
          <div className="w3-accordion w3-light-grey">
            <TagList data={this.props.data.tags} />
          </div>
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <Category data={data} />,
  document.getElementById('content')
);
