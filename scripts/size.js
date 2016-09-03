var SIZES = [90, 120, 180];

var Size = React.createClass({
  propTypes: {
    size: React.PropTypes.number.isRequired,
    onSelect: React.PropTypes.func.isRequired
  },

  render() {
    var size = this.props.size;
    var onSelect = this.props.onSelect;

    return (
      <div>
        {
          _.map(SIZES, function(currentSize) {
            var style = {
              backgroundColor: 'red',
              margin: '5px'
            };

            if (currentSize === size) {
              style.backgroundColor = 'blue';
            };

            return (
              <div
                style={style}
                onClick={function() {
                  onSelect(currentSize);
                }}
              >
                {currentSize}
              </div>
            );
          })
        }
      </div>
    );
  }
});
