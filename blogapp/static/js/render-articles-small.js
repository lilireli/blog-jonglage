var ArticleSmall = React.createClass({
    handleClick: function() {
        window.location = "3-balles.html";
    },
    render: function() {
        return (
          <div className="w3-container w3-margin-bottom w3-pale-blue w3-col s3 article-small" onClick={this.handleClick} >
            <h2>Title</h2>
            <p>Praesent tincidunt sed tellus ut rutrum. Sed vitae justo condimentum, porta lectus vitae, ultricies congue gravida diam non fringilla. Lorem ipsum dolor sit amet et calerare out if ned.</p>
          </div>
        );
    }
});


ReactDOM.render(
  <ArticleSmall />,
  document.getElementById('example')
);
