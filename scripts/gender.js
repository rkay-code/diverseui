var GENDERS = ['BOTH', 'MALE', 'FEMALE'];

var Gender = React.createClass({
  propTypes: {
    gender: React.PropTypes.string.isRequired,
    onSelect: React.PropTypes.func.isRequired
  },

  render() {
    var gender = this.props.gender;
    var onSelect = this.props.onSelect;

    return (
      <div>
        {
          _.map(GENDERS, function(currentGender) {
            var style = {
              backgroundColor: 'red',
              margin: '5px'
            }

            if (currentGender === gender) {
              style.backgroundColor = 'blue';
            }

            return (
              <div
                style={style}
                onClick={function() {
                  onSelect(currentGender);
                }}
              >
                {currentGender}
              </div>
            );
          })
        }
      </div>
    );
  }
});
