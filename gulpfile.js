var gulp  = require('gulp');
var babel = require('gulp-babel');
var open = require('gulp-open');

gulp.task('js', function () {
  return gulp.src('*.js')
    .pipe(babel({
      plugins: ['transform-react-jsx']
    }))
    .pipe(gulp.dest('output'));
});

gulp.task('default', ['js'], function(){
  return gulp.src('./index.html')
    .pipe(open(), {app: 'google-chrome'});
});
