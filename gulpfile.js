var gulp  = require('gulp');
var rename = require('gulp-rename');
var sass = require('gulp-sass');
var watch = require('gulp-watch');

gulp.task('sass', function() {
  return gulp.src('static/styles/*.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(rename(function (path) {
      path.basename += '-compiled';
      path.extname = '.css';
    }))
    .pipe(gulp.dest('static/styles'));
});

gulp.task('sass:watch', function() {
  gulp.watch('static/styles/*.scss', ['sass']);
});

gulp.task('default', ['sass', 'sass:watch']);
