const gulp = require('gulp');
const argv = require('yargs').argv

gulp.task('deploy', () => {
  var from = './services/clients/pi_py/**/*';
  var to = '/Volumes/HOMEPI/pi_py/';
  gulp.src(from)
          .pipe(gulp.dest(to));
});

gulp.task('test', () => {

});
