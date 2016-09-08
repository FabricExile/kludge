USD_ROOT=/opt/pixar/usd \
USD_DEPS_ROOT=/opt/usd-deps \
./kludge discover \
  -C-std=c++11 \
  -D'BUILD_COMPONENT_SRC_PREFIX="pxr/"' \
  -I'${USD_ROOT}/include' \
  -I'${USD_DEPS_ROOT}/include' \
  -I'${USD_DEPS_ROOT}/include/python2.7' \
  -I'${USD_DEPS_ROOT}/include/OpenEXR' \
  -L'${USD_ROOT}/lib' \
  -lusd \
  -lusdGeom \
  -DBUILD_OPTLEVEL_DEV \
  '${USD_ROOT}/include/pxr/usd/usd/stage.h'
