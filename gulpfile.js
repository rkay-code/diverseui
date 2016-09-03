var gulp  = require('gulp');
var connect = require('gulp-connect');
var sass = require('gulp-sass');
var watch = require('gulp-watch');

gulp.task('connect', function() {
  return connect.server({
    livereload: true,
    port: 8080
  });
});

gulp.task('watch', function() {
  return gulp.watch(['scripts/*.js', '*.html', 'styles/*.css'], ['stream']);
});

gulp.task('sass', function() {
  return gulp.src('styles/*.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest('styles'));
});

gulp.task('sass:watch', function() {
  gulp.watch('styles/*.scss', ['sass']);
});

gulp.task('stream', function() {
  return gulp.src('scripts/*.js')
    .pipe(gulp.dest('output'))
    .pipe(connect.reload());
});

gulp.task('default', ['connect', 'sass', 'sass:watch', 'stream', 'watch']);
