var ArticleSmall = React.createClass({
  handleClick: function() {
    window.location = "/articles/" + this.props.data.id;
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

var CategoryTackle = React.createClass({
  render: function() {
    return (
      <div>
        <h1><b>{this.props.data.name}</b></h1>
        <div className="w3-section w3-bottombar"></div>

        <div className="w3-container w3-margin-bottom w3-threequarter">
          <div dangerouslySetInnerHTML={{__html: this.props.data.description}}></div>
        </div>

        <div className="w3-quarter">
            <img src={"/static/img/" + this.props.data.page_type + ".png"}></img>
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

var ArticleSmallLarge = React.createClass({
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

var ArticleSmallLargeList = React.createClass({
  render: function() {
    var articleNodes = this.props.data.map(function(article) {
      return (
        <ArticleSmallLarge data={article} key={article.id} />
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

var CategoryDiary = React.createClass({
  render: function() {
    return (
      <div>
        <h1><b>{this.props.data.name}</b></h1>
        <div className="w3-section w3-bottombar"></div>

        <div className="w3-container w3-margin-bottom">
          <div dangerouslySetInnerHTML={{__html: this.props.data.description}}></div>
        </div>

        <ArticleSmallLargeList data={this.props.data.articles} />

        {/* Pagination */}
        <div className="w3-center w3-padding-32">
          <PageLinkList data={this.props.data.pagination} />
        </div>
      </div>
    );
  }
});

var Category = React.createClass({
  render: function() {
    let contents;
    if (this.props.data.page_type == "todojournal") {
      contents = <CategoryDiary data={data} />
    } else {
      contents = <CategoryTackle data={data} />
    }

    return (
      <div>
        {contents}
      </div>
    )
  }
});

ReactDOM.render(
  <Category data={data} />,
  document.getElementById('content')
);
