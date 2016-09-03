var BOTH = 'BOTH';
var MALE = 'MALE';
var FEMALE = 'FEMALE';

var App = React.createClass({
  propTypes: {
    images: React.PropTypes.array
  },

  getDefaultProps: function() {
    return {
      images: []
    };
  },

  getInitialState: function() {
    return {
      size: 90,
      gender: BOTH
    };
  },

  selectSize: function(newSize) {
    this.setState({
      size: newSize
    });
  },

  selectGender: function(newGender) {
    this.setState({
      gender: newGender
    });
  },

  render: function() {
    var gender = this.state.gender;
    var size = this.state.size;

    var images = _.filter(this.props.images, function(image) {
      return gender === BOTH || image.gender === gender;
    });

    return (
      <div>
        <div>
          <Size size={size} onSelect={this.selectSize} />
          <Gender gender={gender} onSelect={this.selectGender} />
        </div>
        <Images size={size} images={images} />
      </div>
    );
  }
});

var IMAGES = [
  {gender: 'MALE'},
  {gender: 'MALE'},
  {gender: 'MALE'},
  {gender: 'MALE'},
  {gender: 'MALE'},
  {gender: 'MALE'},
  {gender: 'FEMALE'},
  {gender: 'FEMALE'},
  {gender: 'FEMALE'},
  {gender: 'FEMALE'},
];

$(document).ready(function() {
  ReactDOM.render(
    <App images={IMAGES} />,
    document.getElementById('app')
  );
});
