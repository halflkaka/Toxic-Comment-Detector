# react-usa
React component for United States choropleth map


## Demo
[Live Demo](https://react-usa-demo.herokuapp.com/)


## Installation
Using [npm](https://www.npmjs.com/):
```
npm install --save react-usa
```


## Preparation
Please perform the following steps in preparation

**Step 1**: Include [leaflet.js](http://leafletjs.com/)'s CSS file link in the `<head>` section of your `index.html`
```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.2.0/dist/leaflet.css" integrity="sha512-M2wvCLH6DSRazYeZRIm1JnYyh22purTM+FDB5CsyxtQJYeKq83arPe5wgbNmcFXGqiSH2XR8dT/fJISVA1r/zQ==" crossorigin=""/>
```

**Step 2**: Obtain a free `mapboxAccessToken` from [Mapbox](https://www.mapbox.com/). You have to create an account to obtain this token


## Usage
```javascript

import React from 'react';
import ReactUSA from 'react-usa';

class Example extends React.Component {
  render() {
    const mapboxAccessToken = "" // Your access token
    const mapboxType = "streets";
    const position = [37.0902, -95.7129];
    const zoom = 4;
    const data = [
      {
        name: "Nebraska",
        values: [{label: "Capital", val: "Lincoln"}, {label: "Electoral Votes", val: 3}],
        color: "#E31A1C"
      }
    ]
    const stateStyle = { weight: 1, opacity: 1, color: '#666', dashArray: '3', fillOpacity: 0.7 };
    const stateHoverStyle = { weight: 5, color: '#FFF', dashArray: '1', fillOpacity: 0.7 };
    const excludeStates = ["District of Columbia", "Puerto Rico"];

    return (
      <div>

        <ReactUSA
          mapboxAccessToken={mapboxAccessToken} // Required
          mapHeight="800px" // Required
          mapWidth="100%"
          className="container"
          mapboxType={mapboxType}
          mapCenter={position}
          mapZoom={zoom}
          mapScrollZoom={false}
          neighborhoodOn={true}
          tooltip={true}
          tooltipSticky={false}
          data={data}
          stateStyle={stateStyle}
          stateHoverStyle={stateHoverStyle}
          excludeStates={excludeStates}
        />

      </div>
    )
  }
}

export default Example;
```


## Properties
The `ReactUSA` component accepts the following props

Name  | Type | Default | Req/Opt | Description
--- | --- | --- | --- | ---
`mapboxAccessToken` | string | | **Required** | Access Token from [Mapbox](https://www.mapbox.com/)
`mapHeight` | string | | **Required** | Height of the map
`mapWidth` | string | `100%` | Optional | Width of the map. Default value is 100% of the containing element
`className` | string | | Optional | Class name to be applied to the map
`mapboxType` | string | `streets` | Optional | Mapbox provides many types of [map themes](https://www.mapbox.com/maps/). This component supports 5 such themes: `light`, `dark`, `streets`, `outdoors`, and `satellite`. Default value is `streets`
`mapCenter` | array | `[37.0902, -95.7129]` | Optional | Geographical coordinates (latitude and longitude) where the map should be centered. Default value is `[37.0902, -95.7129]`
`mapZoom` | integer | `4` | Optional | Initial zoom level for the map. Default value is `4`
`mapScrollZoom` | boolean | `false` | Optional | Indicates whether the map can be zoomed by using the mouse wheel. Default value is `false`
`statesOn` | boolean | `true` | Optional | Indicates whether the state tiles should be displayed. Default value is `true`
`tooltip` | boolean | `true` | Optional | Indicates whether the tooltip should appear when hovering over a state tile. Default value is `true`
`tooltipSticky` | boolean | `false` | Optional | If `true`, the tooltip will follow the mouse instead of being fixed at the feature center. Default value is `false`
`stateStyle` | object | | Optional | Style of the state tile. This overrides the default style, which is `{ weight: 1, opacity: 1, color: '#666', dashArray: '3', fillOpacity: 0.7 }`
`stateHoverStyle` | object | | Optional | Style of the state tile when hovered over. This overrides the default style, which is `{ weight: 5, color: '#FFF', dashArray: '1', fillOpacity: 0.7 }`
`excludeStates` | array | | Optional | To exclude any states from the map, provide the state names in an array. Default will show all 50 states
`data` | array | | Optional | See the Data section below for details

**Note on hover styles**: To ensure that the tile style behaves as expected when hovered over and away from the tile, please include matching CSS properties in both `stateStyle` and `stateHoverStyle`. For example, if the `fillOpacity` CSS property is defined in `stateStyle`, then please define `fillOpacity` in `stateHoverStyle` as well, and vice versa. Otherwise, some properties assigned during hover will remain even when hovered away and vice versa.


## Data
The `data` prop is an array of objects. Each object is dedicated to a state and must have the following keys:
* `name`: Name of the state
* `values`: Array of objects with keys `label` and `val`
* `color`: Color of the state tile. If color is unspecified, the default color for all tiles is `#FFEDA0`

For example, if you want to highlight the below states with their data, then simply pass the below `data` array of objects.
```javascript
const data = [
  {
    name: "Nebraska",
    values: [{label: "Capital", val: "Lincoln"}, {label: "Electoral Votes", val: 3}],
    color: "#E31A1C"
  },
  {
    name: "Kansas",
    values: [{label: "Population", val: "1.6 Million"}],
    color: "#E31A1C"
  }
]
```

[ColorBrewer](http://colorbrewer2.org/) is a nice tool that helps you choose nice colors for state tiles


## States
There are 50 states along with District of Columbia and Puerto Rico shown on the map

State | State | State | State
--- | --- | --- | ---
Alabama | Indiana | Nebraska | South Carolina
Alaska | Iowa | Nevada | South Dakota
Arizona | Kansas | New Hampshire | Tennessee
Arkansas | Kentucky | New Jersey | Texas
California | Louisiana | New Mexico | Utah
Colorado | Maine | New York | Vermont
Connecticut | Maryland | North Carolina | Virginia
Delaware | Massachusetts | North Dakota | Washington
Florida | Michigan | Ohio | West Virginia
Georgia | Minnesota | Oklahoma | Wisconsin
Hawaii | Mississippi | Oregon | Wyoming
Idaho | Missouri | Pennsylvania | District of Columbia
Illinois | Montana | Rhode Island | Puerto Rico


## License
MIT


## Credits
* [Leaflet.js](http://leafletjs.com/)
* [react-leaflet](https://github.com/PaulLeCam/react-leaflet)
* [Mapbox](https://www.mapbox.com/)
* [Who's On First](https://whosonfirst.mapzen.com/) by [Mapzen](https://mapzen.com/)
