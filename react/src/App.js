import React from 'react';
import {PieChart, BarChart, Legend} from 'react-easy-chart';
import { Button, Grid, Row} from 'react-bootstrap';

export default class App extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        error: null,
        isLoaded: false,
        items: [
          { key: 'A', value: 100 },
          { key: 'B', value: 200 },
          { key: 'C', value: 50 }
        ],
        bar: [
          {x: 'A', y:100},
          { x: 'B', y: 200 },
          { x: 'C', y: 50 }
        ]
      };
      this.refresh = this.refresh.bind(this);
  }
  refresh() {
    this.setState({
      isLoaded : false
    });
    fetch("http://localhost:5000/refresh")
        .then(res => res.json())
        .then(
          (result) => {
            console.log("res: " + result);
            this.setState({
              isLoaded: true,
              items: result[0],
              bar: result[1]
            });
          },
          (error) => {
            this.setState({
              isLoaded: true,
              error: error
            });
          }
        )
  }
  componentDidMount() {
      this.refresh();
  }
  render () {
    const { error, isLoaded, items, bar } = this.state;
    if (error) {
        return <div>Error: {error.message}</div>;
    } else {
      console.log("draw...");
      console.log(items);
      return (
      <Grid>
         <Row className="text-center">
            <h1>Toxic Comment Classification</h1>
         </Row>
         <Row className="text-center">
             <div style={{display: 'inline-block'}}>
                   <BarChart axes colorBars grid
                              height={350}
                              width={650}
                              data={bar}
                              clickHandler={(d) => this.setState({barDataDisplay: `The value on the ${d.x} is ${d.y}`})}/>
            </div>
          </Row>
          <Row>
            <div style={{display: 'inline-block', verticalAlign: 'top', paddingLeft: '20px'}}>
                {this.state.barDataDisplay ? this.state.barDataDisplay : 'Click on a bar to show the value'}
            </div>
         </Row>
         <Row className="text-center">
             <div style={{display: 'inline-block'}}>
              <PieChart labels data={items} clickHandler={
                  (d) => this.setState({
                    dataDisplay: `The value of ${d.data.key} is ${d.value}`
                  })
              }/>
              <Legend data={items} dataId={'key'} horizontal />
              </div>
          </Row>
          <Row>
            <div style={{display: 'inline-block', verticalAlign: 'top', paddingLeft: '20px'}}>
              {this.state.dataDisplay ? this.state.dataDisplay : 'Click on a bar to show the value'}
            </div>
         </Row>

         <Row className="text-center">
         <div style={{display: 'inline-block', verticalAlign: 'top', paddingLeft: '20px'}}>
            <Button bsStyle="primary" onClick={this.refresh}>{isLoaded? 'Refresh':'Loading'}</Button>
          </div>
         </Row>
      </Grid>
      );
    }
  }
}
