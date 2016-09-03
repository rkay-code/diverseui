var App = React.createClass({
  getInitialState: function() {
    return {
      color: 'red',
      size: 100
    };
  },

  changeColor: function() {
    this.setState({
      color: 'blue'
    });
  },

  render: function() {
    var _this = this;
    var size = this.state.size;
    var color = this.state.color;

    var style = {
      backgroundColor: color
    };

    return (
      <div>
        <img onClick={function() { _this.setState({size: _this.state.size + 100}); }} width={size} height={size} src="https://i.imgur.com/MzxkAeG.jpg" />
        <h1 onClick={this.changeColor} style={style}>hi</h1>
      </div>
    );
  }
});

ReactDOM.render(
  <App />,
  document.getElementById('app')
);
