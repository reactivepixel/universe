## Data Flow

### Broker

* On Harness (long-term move to app)

### Clients

* Web
* iOS app
* Android App

## Ctrl Rooms

* DeviceCtrl
* VenueCtrl
* GroupCtrl
* MasterCtrl

## Data Structure

```javascript
{
	playlist: {
		id: 'xxxx-xxxx-xxxx-xxxx',
    arrangements: [{
      id: 'xxxx-xxxx-xxxx-xxxx',
      orderIndex: 0,
      cycles: 2,
      principleTrack: {
        id: 'xxxx-xxxx-xxxx-xxxx',
        file: '/path/to/file'
      },
      tracks: [{
        id: 'xxxx-xxxx-xxxx-xxxx',
        position: 0,
        file: '/path/to/file'
      }]
    }]
	}
}
```

# RPI installs

* ```sudo pip install paho-mqtt```
