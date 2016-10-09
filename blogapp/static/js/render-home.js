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
    window.location = "/articles/" + this.props.data.id;
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

var PageLink = React.createClass({
  render: function() {
    var link = (<a className={((this.props.current == this.props.number) ? "w3-black" : "w3-hover-black")} href={this.props.link}>{this.props.number}</a>);
    var linkSmaller = (<a className="w3-hover-black" href={this.props.link}>«</a>);
    var linkBigger = (<a className="w3-hover-black" href={this.props.link}>»</a>);
    var linkNone = "";

    /* Do not render all pages number */
    if (this.props.number != 1 && this.props.number != this.props.max ){ /* Page 1 and last page are always rendered */
      /* Small pages */
      if (this.props.current > 5){
        if (this.props.current > this.props.max - 3){
          if (this.props.number == this.props.max - 5){
            link = linkSmaller; /* Insert << */
          }
          else if (this.props.number < this.props.max - 5 ){
            link = linkNone; /* Number is too small */
          }
        }
        else {
          if (this.props.number == this.props.current - 3){
            link = linkSmaller; /* Insert << */
          }
          else if (this.props.number < this.props.current - 3 ){
            link = linkNone; /* Number is too small */
          }
        }
      }
      /* Big pages */
      if (this.props.current < this.props.max - 4){
        if (this.props.current < 4){
          if (this.props.number == 6){
            link = linkBigger; /* Insert >> */
          }
          else if (this.props.number > 6){
            link = linkNone; /* Number is too big */
          }
        }
        else {
          if (this.props.number == this.props.current + 3){
            link = linkBigger; /* Insert >> */
          }
          else if (this.props.number > this.props.current + 3){
            link = linkNone; /* Number is too big */
          }
        }
      }
    }
    return (
      <li>
        {link}
      </li>
    );
  }
});

var PageLinkList = React.createClass({
  render: function() {
    var current_page = this.props.data.current_page;
    var nb_page = this.props.data.nb_page;
    var pageNodes = this.props.data.pages.map(function(page) {
      return (
        <PageLink number={page.number} link={page.link} key={page.number} current={current_page} max={nb_page} />
      );
    });
    return (
      <ul className="w3-pagination">
        {pageNodes}
      </ul>
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
          <PageLinkList data={this.props.data.pagination} />
        </div>
      </div>
    );
  }
});

ReactDOM.render(
  <Home data={data} />,
  document.getElementById('content')
);
