var Tags = React.createClass({
  render: function() {
    var tagNodes = this.props.data.map(function(tag) {
      return (
        <span className="w3-dark-grey w3-round-xlarge w3-padding-small margin-small-right">{tag.name}</span>
      );
    });
    return (
      <span className="tagList">
        {tagNodes}
      </span>
    );
  }
});

var Article = React.createClass({
    render: function() {
        return (
          <div>
            <p>
              <span className="w3-teal w3-padding-small uppercase margin-small-right">{this.props.data.category}</span>
              <Tags data={this.props.data.tags} />
            </p>
            <h1><b>{this.props.data.name}</b></h1>
            <p className="w3-text-grey">Par <b>{this.props.data.author}</b> le {this.props.data.creation_date} (modifié le {this.props.data.last_modification_date})</p>
            <div className="w3-section w3-bottombar"></div>

            <div dangerouslySetInnerHTML={{__html: this.props.data.content}}></div>
          </div>
        );
    }
});

ReactDOM.render(
  <Article data={data} />,
  document.getElementById('content')
);

$('nav-container').addClass(data.category);
