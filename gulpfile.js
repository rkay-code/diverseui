var gulp  = require('gulp');
var babel = require('gulp-babel');
var connect = require('gulp-connect');
var watch = require('gulp-watch');

gulp.task('connect', function() {
  return connect.server({
    livereload: true,
    port: 8080
  });
});

gulp.task('watch', function() {
  return gulp.watch(['scripts/*.js'], ['stream']);
})

gulp.task('stream', function() {
  return gulp.src('scripts/*.js')
    .pipe(babel({
      plugins: ['transform-react-jsx']
    }))
    .pipe(gulp.dest('output'))
    .pipe(connect.reload());
});

gulp.task('default', ['connect', 'stream', 'watch']);
