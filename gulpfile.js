var gulp  = require('gulp');
var babel = require('gulp-babel');
var connect = require('gulp-connect');
var watch = require('gulp-watch');

gulp.task('connect', function() {
  connect.server({
    livereload: true,
    port: 8080
  });
});

gulp.task('watch', function() {
  gulp.watch(['*.js'], ['stream']);
})

gulp.task('stream', function () {
    return gulp.src('*.js')
    .pipe(babel({
      plugins: ['transform-react-jsx']
    }))
    .pipe(gulp.dest('output'))
    .pipe(connect.reload());
});

gulp.task('default', ['connect', 'stream', 'watch']);
