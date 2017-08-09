const express = require('express');

module.exports = () => {
  const router = express.Router();

  router.get('/status', (req, res) => {
    res.json({
      hello: true,
    });
  });


  router.get('/', (req, res) => {
    const payload = {
      menus: [{
        title: 'General',
        items: [
          { title:'Dashboard', icon: 'md-view-dashboard', link: 'javascript:void(0)' },
          { title:'Settings', icon: 'md-view-dashboard', link: 'javascript:void(0)' },
        ]
      }],
      gauges: [
        {title: 'Battery', context: 'progress-bar-warning', value: '75%'}
      ],
      listGroups: [{
        title: 'Playlists',
        items: [
            { title:'None', icon: 'md-view-dashboard', link: 'javascript:void(0)', active: true },
            // No Playlists defined yet
            // TODO Define and config playlists
            // { title:'Rainbow', icon: 'md-link', link: 'javascript:void(0)', active: false },
            // { title:'Blue Gate', icon: 'md-view-dashboard', link: 'javascript:void(0)', active: false },
            // { title:'Franks', icon: 'md-link', link: 'javascript:void(0)', active: false },
          ]
        }]
      }

    res.render('dashboard', payload);
  });

  return router;
};
