./kludge discover \
  -I/opt/pixar/usd/include \
  -I/opt/usd-deps/include \
  -I/opt/usd-deps/include/python2.7 \
  -I/opt/usd-deps/include/OpenEXR/ \
  -DBUILD_COMPONENT_SRC_PREFIX='"pxr/"' \
  -DBUILD_OPTLEVEL_DEV \
  -C -std=c++11 \
  --ignore-dir /opt/pixar/usd/include/pxr/imaging \
  Test /opt/pixar/usd/include/pxr/
