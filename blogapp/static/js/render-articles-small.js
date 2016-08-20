var ArticleSmall = React.createClass({
    handleClick: function() {
        window.location = this.props.url;
    },
    render: function() {
        return (
          <div className="w3-container w3-col s3 w3-padding">
            <div className="w3-container w3-pale-blue article-small" onClick={this.handleClick}>
              <h2>{this.props.name}</h2>
              <p>{this.props.description}</p>
            </div>
          </div>
        );
    }
});


var ArticleSmallList = React.createClass({
  render: function() {
    var articleNodes = this.props.data.map(function(article) {
      return (
        <ArticleSmall url={article.url} name={article.name} description={article.description} key={article.name} />
      );
    });
    return (
      <div className="articleList">
        {articleNodes}
      </div>
    );
  }
});

ReactDOM.render(
  <ArticleSmallList data={data} />,
  document.getElementById('content')
);
