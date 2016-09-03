var Images = React.createClass({
  propTypes: {
    size: React.PropTypes.number.isRequired,
    images: React.PropTypes.array.isRequired
  },

  render() {
    var size = this.props.size;
    var images = this.props.images;

    return (
      <div>
        {
          _.map(images, function(image) {
            var style = {
              display: 'inline-block',
              height: size,
              margin: '30px',
              width: size
            };

            return (
              <img
                style={style}
                src={image.src}
              />
            );
          })
        }
      </div>
    );
  }
});
