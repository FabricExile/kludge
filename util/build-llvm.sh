#!/bin/bash

VER=$1
if [ -z "$VER" ]; then
  echo "Usage: $0 <LLVM version>"
  exit 1
fi

set -ev

SVN_ROOT=http://llvm.org/svn/llvm-project
TAG=tags/RELEASE_$(echo $VER | tr -d '.')/final
svn co $SVN_ROOT/llvm/$TAG llvm-$VER
svn co $SVN_ROOT/cfe/$TAG llvm-$VER/tools/clang
svn co $SVN_ROOT/clang-tools-extra/$TAG llvm-$VER/tools/clang/tools/extra
svn co $SVN_ROOT/compiler-rt/$TAG llvm-$VER/projects/compiler-rt
svn co $SVN_ROOT/libcxx/$TAG llvm-$VER/projects/libcxx
svn co $SVN_ROOT/libcxxabi/$TAG llvm-$VER/projects/libcxxabi
svn revert -R llvm-$VER/projects/libcxxabi
if [ "$VER" = "3.5.2" ]; then
  patch -d llvm-$VER/projects/libcxxabi -p2 <<EOF
Index: libcxxabi/trunk/src/cxa_default_handlers.cpp
===================================================================
--- libcxxabi/trunk/src/cxa_default_handlers.cpp
+++ libcxxabi/trunk/src/cxa_default_handlers.cpp
@@ -101,19 +101,21 @@
 unexpected_handler
 set_unexpected(unexpected_handler func) _NOEXCEPT
 {
-	if (func == 0)
-		func = default_unexpected_handler;
-	return __sync_swap(&__cxa_unexpected_handler, func);
+    if (func == 0)
+        func = default_unexpected_handler;
+    return __atomic_exchange_n(&__cxa_unexpected_handler, func,
+                               __ATOMIC_ACQ_REL);
 //  Using of C++11 atomics this should be rewritten
 //  return __cxa_unexpected_handler.exchange(func, memory_order_acq_rel);
 }
 
 terminate_handler
 set_terminate(terminate_handler func) _NOEXCEPT
 {
-	if (func == 0)
-		func = default_terminate_handler;
-	return __sync_swap(&__cxa_terminate_handler, func);
+    if (func == 0)
+        func = default_terminate_handler;
+    return __atomic_exchange_n(&__cxa_terminate_handler, func,
+                               __ATOMIC_ACQ_REL);
 //  Using of C++11 atomics this should be rewritten
 //  return __cxa_terminate_handler.exchange(func, memory_order_acq_rel);
 }
Index: libcxxabi/trunk/src/cxa_handlers.cpp
===================================================================
--- libcxxabi/trunk/src/cxa_handlers.cpp
+++ libcxxabi/trunk/src/cxa_handlers.cpp
@@ -102,14 +102,14 @@
     __terminate(get_terminate());
 }
 
-extern "C" new_handler __cxa_new_handler = 0;
+new_handler __cxa_new_handler = 0;
 // In the future these will become:
 // std::atomic<std::new_handler>  __cxa_new_handler(0);
 
 new_handler
 set_new_handler(new_handler handler) _NOEXCEPT
 {
-    return __sync_swap(&__cxa_new_handler, handler);
+    return __atomic_exchange_n(&__cxa_new_handler, handler, __ATOMIC_ACQ_REL);
 //  Using of C++11 atomics this should be rewritten
 //  return __cxa_new_handler.exchange(handler, memory_order_acq_rel);
 }
EOF
fi

CMAKE_DEFS=
case $OSTYPE in
  linux*)
    GCC_ROOT=/opt/gcc-4.8
    CMAKE_DEFS="$CMAKE_DEFS -DCMAKE_C_COMPILER=$GCC_ROOT/bin/gcc"
    CMAKE_DEFS="$CMAKE_DEFS -DCMAKE_CXX_COMPILER=$GCC_ROOT/bin/g++"
    CMAKE_DEFS="$CMAKE_DEFS -DCMAKE_EXE_LINKER_FLAGS=\"-L$GCC_ROOT/lib64 -Wl,-rpath,$GCC_ROOT/lib64\""
    CMAKE_DEFS="$CMAKE_DEFS -DCMAKE_SHARED_LINKER_FLAGS=\"-L$GCC_ROOT/lib64 -Wl,-rpath,$GCC_ROOT/lib64\""
    CMAKE_DEFS="$CMAKE_DEFS -DCMAKE_MODULE_LINKER_FLAGS=\"-L$GCC_ROOT/lib64 -Wl,-rpath,$GCC_ROOT/lib64\""
    CMAKE_DEFS="$CMAKE_DEFS -DGCC_INSTALL_PREFIX=$GCC_ROOT"
    CMAKE_DEFS="$CMAKE_DEFS -DPYTHON_EXECUTABLE=/opt/python-2.7.10/bin/python2.7"
    NPROC=$(nproc)
    ;;
  darwin*)
    NPROC=$(sysctl -n hw.ncpu)
    ;;
esac
rm -rf llvm-$VER/build
mkdir -p llvm-$VER/build
cd llvm-$VER/build
cmake .. \
  $CMAKE_DEFS \
  -DCMAKE_INSTALL_PREFIX=/opt/llvm-$VER \
  -DCMAKE_BUILD_TYPE="Release" \
  -DLLVM_TARGETS_TO_BUILD="X86"
make -j$NPROC
cd ../..
sudo make -C llvm-$VER/build install
sudo mkdir /opt/llvm-$VER/lib/python
sudo cp -r llvm-$VER/tools/clang/bindings/python/clang /opt/llvm-$VER/lib/python/
