var Tags = React.createClass({
  render: function() {
    var tagNodes = this.props.data.map(function(tag) {
      return (
        <span className="w3-dark-grey w3-round-xlarge w3-padding-small margin-small-right">{tag.name}</span>
      );
    });
    return (
      <span>
        {tagNodes}
      </span>
    );
  }
});

var ArticleSmall = React.createClass({
  handleClick: function() {
    window.location = this.props.id;
  },
  render: function() {
    return (
      <div className="w3-container w3-margin-bottom w3-white">
        <div className="w3-container article-small" onClick={this.handleClick}>
          <h2>{this.props.data.name}</h2>
          <p className="w3-text-grey">
            <span className="margin-small-right">Le {this.props.data.creation_date} sous</span>
            <span className="w3-teal w3-padding-small uppercase margin-small-right">{this.props.data.category}</span>
            <Tags data={this.props.data.tags} />
          </p>
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
      <div className="w3-container">
        {articleNodes}
      </div>
    );
  }
});

var Home = React.createClass({
  render: function() {
    return (
      <div>
        <h1><b>Nos derniers articles</b></h1>
        <div className="w3-section w3-bottombar"></div>

        <ArticleSmallList data={this.props.data.articles} />

        {/* Pagination */}
        <div className="w3-center w3-padding-32">
          <ul className="w3-pagination">
            <li><a className="w3-black" href="#">1</a></li>
            <li><a className="w3-hover-black" href="#">2</a></li>
            <li><a className="w3-hover-black" href="#">3</a></li>
            <li><a className="w3-hover-black" href="#">4</a></li>
            <li><a className="w3-hover-black" href="#">»</a></li>
          </ul>
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <Home data={data} />,
  document.getElementById('content')
);
