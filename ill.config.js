module.exports = {
  apps : [
    {
      name      : 'broker',
      script    : 'services/broker/server.js',
      env: {
        HOST: "localhost",
        MQTT_PORT: "1883",
        MQTT_CONN_STR: "mqtt://localhost:1883",
        DEVICE_ID: "apex-0000-0000-0001",
        GROUP_ID: "PirateShip",
        VENUE_ID: "home-0000-0000-0001"
      },
    },

    {
      name      : 'client',
      script    : 'services/clients/restful-bridge/server.js',
      env: {
        HOST: "localhost",
        MQTT_PORT: "1883",
        MQTT_CONN_STR: "mqtt://localhost:1883",
        DEVICE_ID: "apex-0000-0000-0001",
        GROUP_ID: "PirateShip",
        VENUE_ID: "home-0000-0000-0001"
      },
    },
  ],
};
