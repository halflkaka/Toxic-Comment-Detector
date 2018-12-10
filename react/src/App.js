import React from 'react';
import {PieChart, BarChart, Legend} from 'react-easy-chart';
import { Button, Grid, Row, Col} from 'react-bootstrap';
import ReactTable from 'react-table'
import '../node_modules/react-table/react-table.css'
import './App.css'
// import {BootstrapTable, TableHeaderColumn} from 'react-bootstrap-table';
// import '../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css';

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
        ],
        blacklist:[{'obscene':[]}]
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
              bar: result[1],
              blacklist: result[2]
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
    const { error, isLoaded, items, bar, blacklist } = this.state;
    console.log(blacklist)
    const columns = [{
      Header: 'Name',
      accessor: 'name',
      width: 500, // String-based value accessors!
      height: 500
    }, {
      Header: 'Tweet',
      accessor:'tweet',
      width: 500,
      height: 500
    }];
    const customStyle = {
      '.legend': {
        margin: 10
      }
    };
    if (error) {
        return <div>Error: {error.message}</div>;
    } else {
      console.log("draw...");
      console.log(items);
      return (
        <div>
      <Grid>
         <Row>
         <Col md={3}/>
         <Col md={6}>
            <h1>Toxic Comment Classification</h1>
          </Col>
          <Col md={4}/>
         </Row>
         <Row>
          <Col md={5}/>
          <Col md={6}>
             <Button bsStyle="primary" onClick={this.refresh}>{isLoaded? 'Refresh':'Loading'}</Button>
          </Col>
          <Col md={4}/>
          </Row>
         <Row>
         <Col md={1}/>
         <Col md={8}>
              <BarChart axes colorBars grid
                  height={550}
                  width={850}
                  data={bar}
                  clickHandler={(d) => this.setState({barDataDisplay: `The value on the ${d.x} is ${d.y}`, selected:d.x})}/>
        </Col>
        <Col md={3}/>
        </Row>
          <Row>
          <Col md={4} />
          <Col md={5}>
                {this.state.barDataDisplay ? this.state.barDataDisplay : 'Click on a bar to show the value'}
            </Col>
          <Col md={5}/>
         </Row>
         <Row/>
          <div/>
         <Row>
          <Col md={3}/>
          <Col md={6}>
              <PieChart data={items} clickHandler={
                  (d) => this.setState({
                    dataDisplay: `The value of ${d.data.key} is ${d.value}`,
                    selected: d.data.key
                  })
              }/>
          </Col>
          <Col md={4}/> 
          </Row>
          <Row>
            <Col md={2}/>
            <Col md={7}>
              <Legend styles={customStyle} data={items} dataId={'key'} horizontal />
            </Col>
            <Col md={5}/>
          </Row>
          <Row>
            <Col md={4} />
            <Col md={4}>
              {this.state.dataDisplay ? this.state.dataDisplay : 'Click on a bar to show the value'}
              </Col>
            <Col md={5}/>
         </Row>

         <Row>
            {this.state.selected? 
              <ReactTable defaultPageSize={10} minRows={10} showPageSizeOptions={false} data={blacklist['0'][this.state.selected]} columns={columns}/>
              : ''}
          </Row>
      </Grid>
      </div>
      );
    }
  }
}
