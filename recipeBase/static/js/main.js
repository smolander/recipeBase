
'use strict';
//const element = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return 'You liked this.';
    }

    return React.createElement(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      'Like'
    );
  }
}

class IngredientTextBox extends React.Component {
  constructor(props) {
    super(props)
    this.state = { ingredients: [],
                   ingredientTemp: '',
                   qtyTemp: ''};
    this.handleAddIngredient = this.handleAddIngredient.bind(this);
    this.onFieldChange = this.onFieldChange.bind(this);
  }

  render() {
    console.log("Rendering text boxes")
    return <div className="IngredientTextBox">
                  <label htmlFor="ingredientTemp">Ingredienser: </label>
                  {this.state.ingredients.map((ingredient) => <p key={ingredient[1]}>{ingredient[0]}, {ingredient[1]}</p>)}
                  <input type="number" name="qtyTemp" value={this.state.qtyTemp} onChange={this.onFieldChange} />
                  <input type="text" name="ingredientTemp" value={this.state.ingredientTemp} onChange={this.onFieldChange} />
                  <input type="button" value="+" onClick={this.handleAddIngredient} />
                </div>;
  }

  onFieldChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleAddIngredient(event) {
    const newIngredient = [this.state.qtyTemp, this.state.ingredientTemp]
    this.setState({
      ingredients: this.state.ingredients.concat([newIngredient]),
      ingredientTemp: '',
      qtyTemp: ''
    });
  }
}

//const domContainer = document.querySelector('#like_button_container');
console.log("Running script")
ReactDOM.render(React.createElement(LikeButton), document.querySelector('#like_button_container'));
ReactDOM.render(React.createElement(IngredientTextBox), document.getElementById("ingredient_boxes"));