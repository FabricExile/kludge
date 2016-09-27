//
// Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
//

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

#if defined _WIN32
#   if defined LIB_STATIC
#       define LIB_EXPORT
#   elif defined DLL_EXPORT
#       define LIB_EXPORT __declspec(dllexport)
#   else
#       define LIB_EXPORT __declspec(dllimport)
#   endif
#else
#   if defined __SUNPRO_C  || defined __SUNPRO_CC
#       define LIB_EXPORT __global
#   elif (defined __GNUC__ && __GNUC__ >= 4) || defined __INTEL_COMPILER
#       define LIB_EXPORT __attribute__ ((visibility("default")))
#   else
#       define LIB_EXPORT
#   endif
#endif

LIB_EXPORT int lib_msg_init (char *msg);
LIB_EXPORT int lib_msg_init_size (char *msg, size_t size);

#ifdef __cplusplus
}
#endif
