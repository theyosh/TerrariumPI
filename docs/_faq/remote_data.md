---
title: How to use remote data
categories: [Website, FAQ]
tags: [remote, API]
---
It is possible to use remote data with TerrariumPI. At the moment, only JSON and plain text are supported as content types.

### Rate limits

If you use a sensor, relay or any other remote service, make sure that the other side can handle a request **every 30 seconds**. This is the frequency of the updates.

### Url format

The remote data url is a full url to the JSON output appended with a dash '#' and the JSON traversal path
`http(s)://remote.server.com:portnumber/path_to_json_output#json/traversal/path`

### Example

Remote source url: `https://terrarium.theyosh.nl/api/sensors/e39b7d7931f8db191cedd83f3c80cec4/`

json output:

```json
{
  "id": "e39b7d7931f8db191cedd83f3c80cec4",
  "hardware": "owfs",
  "type": "temperature",
  "name": "Midden links",
  "address": "2653D18D0100006A",
  "limit_min": 10,
  "limit_max": 45,
  "alarm_min": 20,
  "alarm_max": 30,
  "max_diff": 0,
  "exclude_avg": false,
  "calibration": {
    "offset": 0
  },
  "value": 23.7188,
  "alarm": false,
  "error": false
}
```

json traversal path: `value`

Construct full url by combining the remote source url and the json traversal path joining by a dash '#'. Full remote source url: `https://terrarium.theyosh.nl/api/sensors/e39b7d7931f8db191cedd83f3c80cec4/#value` and that will return the value of '23.7188'

And for the calibration offset value you need the path `#calibration/offset`
